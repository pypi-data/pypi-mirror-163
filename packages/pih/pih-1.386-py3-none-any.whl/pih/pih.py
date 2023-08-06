import abc
import calendar
from dataclasses import dataclass
from datetime import datetime
import enum
from getpass import getpass
import locale
import os
import re
import subprocess
import sys
from typing import Any, Callable, Dict, Generic, List, Tuple, TypeVar
import colorama
from colorama import Back, Style
from prettytable import PrettyTable
import win32com.client

#sys.path.append("//pih/facade")
from pih.collection import CommandChainItem, CommandLinkItem, FieldItem, CommandItem, FieldItemList, FullName, LoginPasswordPair, PasswordSettings
from pih.const import CONST, EXECUTOR, FIELD_NAME_COLLECTION, LOCAL_COMMAND_LIST_DICT, FIELD_COLLECTION, PASSWORD, PATHS
from pih.rpc_commnads import RPC_COMMANDS
from pih.tools import DataTools, ResultUnpack, FullNameTool, PasswordTools


class NotImplemented(BaseException):
    pass


class NotFound(BaseException):
    pass


class UserInterruption(BaseException):
    pass


class CommandNameIsExistsAlready(BaseException):
    pass


class CommandFullFileNameIsExistAlready(Exception):
    pass


class CommandNameIsNotExists(Exception):
    pass


@dataclass
class Command:
    group: str
    command_name: str
    file: str
    description: str
    section: str
    cyclic: bool
    confirm_for_continue: bool = True


@dataclass
class CommandLink:
    command_name: str
    data_extractor_name: str


@dataclass
class CommandChain:
    name: str
    input_name: str
    description: str
    list: List[CommandLink]
    confirm_for_continue: bool = True
    enable: bool = True


T = TypeVar('T')


class GenericCommandList(Generic[T]):

    def __init__(self):
        self.command_list: List[T] = []
        self.name_dict: Dict[str, T] = {}
        self.index_dict: Dict[int, str] = {}
        self.index = 0

    def length(self) -> int:
        return len(self.command_list)

    def get_by_index(self, index: int) -> T:
        return self.name_dict[self.index_dict[index]]

    def get_by_name(self, name: str) -> T:
        name = name.lower()
        for key in self.name_dict:
            key_lower = key.lower()
            if key_lower == name:
                return self.name_dict[key]
        #raise KeyError
        return None

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index > self.length():
            self.index = 0
            raise StopIteration
        return self.index, self.get_by_index(self.index - 1)


class CommandList(GenericCommandList[Command]):

    def register(self, command: Command) -> None:
        def get_command_file_name(command: Command) -> str:
            return command.group + command.file + command.section
        if command.command_name in map(lambda item: item.command_name, self.command_list):
            raise CommandNameIsExistsAlready()
        if get_command_file_name(command) in map(lambda item: get_command_file_name(item), self.command_list):
            raise CommandFullFileNameIsExistAlready(
                f"{command.command_name}: {get_command_file_name(command)}")
        self.command_list.append(command)
        self.name_dict[command.command_name] = command
        self.index_dict[self.length() - 1] = command.command_name


class CommandChainList(GenericCommandList[CommandChain]):

    def register(self, item: CommandChain) -> None:
        if item.name in map(lambda item: item.name, self.command_list):
            raise CommandNameIsExistsAlready()
        self.command_list.append(item)
        self.name_dict[item.name] = item
        self.index_dict[self.length() - 1] = item.name


class ICommandListStorage(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "get_command_list") and
                callable(subclass.get_command_list) or
                NotImplemented)

    @abc.abstractmethod
    def get_command_list(self) -> CommandList:
        raise NotImplemented


class IInfoOwner(metaclass=abc.ABCMeta):

    PARAMS: str = "--info"

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "get_info") and
                callable(subclass.get_info) or
                NotImplemented)

    @abc.abstractmethod
    def get_info(self) -> Dict:
        raise NotImplemented


class CommandTools:

    @staticmethod
    def get_command_group_path(command: Command) -> str:
        return f"{CONST.FACADE.PATH}{command.group}{CONST.FACADE.COMMAND_SUFFIX}"

    @staticmethod
    def get_file_extension(file: str) -> str:
        return "" if file.find(".") == -1 else file.split(".")[-1]

    @staticmethod
    def convert_command_to_command_file_path(command: Command) -> str:
        shell = win32com.client.Dispatch("WScript.Shell")
        return shell.CreateShortCut(command.file).Targetpath if CommandTools.get_file_extension(command.file) == "lnk" else command.file

    @staticmethod
    def get_executor_path(path: str) -> str:
        return EXECUTOR.get(CommandTools.get_file_extension(path))

    @staticmethod
    def convert_command_file_path_for_executor(path: str, executor: str) -> str:
        if executor == EXECUTOR.POWERSHELL_EXECUTOR or executor == EXECUTOR.VBS_EXECUTOR:
            path = f".\\{path}"
        return path

    @staticmethod
    def set_cwd(path: str) -> None:
        os.chdir(path)

    @staticmethod
    def check_for_command_paths_exsit(command: Command):
        command_group_directory_path = CommandTools.get_command_group_path(
            command)
        if not os.path.exists(command_group_directory_path):
            return CommandPathExsitsStatus.COMMAND_GROUP_DIRECTORY_IS_NOT_EXSITS
        CommandTools.set_cwd(command_group_directory_path)
        command.file = CommandTools.convert_command_to_command_file_path(
            command)
        if not os.path.exists(command.file):
            return CommandPathExsitsStatus.COMMAND_FILE_IS_NOT_EXSITS
        command.file = CommandTools.convert_command_file_path_for_executor(
            command.file, CommandTools.get_executor_path(command.file))
        return CommandPathExsitsStatus.OK
#


class CommandPathExsitsStatus(enum.Enum):
    OK: int = 0
    COMMAND_GROUP_DIRECTORY_IS_NOT_EXSITS: int = 1
    COMMAND_FILE_IS_NOT_EXSITS: int = 2


class LocalCommandListStorage(ICommandListStorage):

    def __init__(self, command_list_dict: dict = LOCAL_COMMAND_LIST_DICT):
        self.command_list_dict = command_list_dict
        self.command_list: CommandList = CommandList()
        self.command_chain_list: CommandChainList = CommandChainList()
        for command_name in self.command_list_dict:
            command_item_obj: Any = self.command_list_dict[command_name]
            if isinstance(command_item_obj, CommandItem):
                command_item: CommandItem = command_item_obj
                if command_item.enable:
                    command: Command = self.convert_to_command(
                        command_name, command_item)
                    try:
                        command_paths_exsits_check_status = CommandTools.check_for_command_paths_exsit(
                            command)
                        if command_paths_exsits_check_status == CommandPathExsitsStatus.COMMAND_GROUP_DIRECTORY_IS_NOT_EXSITS:
                            PR.red(
                                f"Command {command.command_name}: group directory is not exsits!")
                        elif command_paths_exsits_check_status == CommandPathExsitsStatus.COMMAND_FILE_IS_NOT_EXSITS:
                            PR.red(
                                f"Command {command.command_name}: file is not exsits!")
                        elif command_paths_exsits_check_status == CommandPathExsitsStatus.OK:
                            self.command_list.register(command)
                    except CommandFullFileNameIsExistAlready:
                        PR.red(
                            f"Command: {command.command_name} is already exsits!")
        for command_name in self.command_list_dict:
            command_item_obj: Any = self.command_list_dict[command_name]
            if isinstance(command_item_obj, CommandChainItem):
                command_chain_item: CommandChainItem = self.command_list_dict[command_name]
                if command_chain_item.enable:
                    if self.command_list.get_by_name(command_name) is None:
                        try:
                            self.command_chain_list.register(
                                self.convert_to_command_chain(command_name, command_chain_item))
                        except CommandNameIsNotExists as error:
                            PR.red(
                                f"Command {command_name}: command link: {error} is not exsits!")
                    else:
                        PR.red(
                            f"Command: {command_chain_item.name} is already exsits!")

    def convert_to_command(self, name: str, command_item: CommandItem) -> Command:
        if name not in self.command_list_dict:
            raise CommandNameIsNotExists
        return Command(command_item.group, name,
                       command_item.file_name,
                       command_item.description,
                       command_item.section,
                       command_item.cyclic)

    def convert_to_command_chain(self, name: str, command_chain_item: CommandChainItem) -> CommandChain:
        if name not in self.command_list_dict:
            raise CommandNameIsNotExists
        list_command_chain: List[CommandChain] = []
        for link_item_obj in command_chain_item.list:
            link_item: CommandLinkItem = link_item_obj
            if self.command_list.get_by_name(link_item.command_name) is not None:
                list_command_chain.append(CommandLink(
                    link_item.command_name, link_item.data_extractor_name))
            else:
                raise CommandNameIsNotExists(link_item.command_name)
        return CommandChain(name,
                            command_chain_item.input_name,
                            command_chain_item.description,
                            list_command_chain,
                            command_chain_item.confirm_for_continue,
                            command_chain_item.enable)

    def get_command_list(self) -> CommandList:
        return self.command_list

    def get_command_chain_list(self) -> CommandChainList:
        return self.command_chain_list

class NamePolicy:

    @staticmethod
    def get_first_letter(name: str) -> str:
        from transliterate import translit
        return translit(name[0], 'ru', reversed=True).lower()
    
    @staticmethod
    def convert_to_login(full_name: FullName) -> FullName:
        return FullName(
            NamePolicy.get_first_letter(
                full_name.last_name),
            NamePolicy.get_first_letter(
                full_name.first_name),
            NamePolicy.get_first_letter(full_name.middle_name))

    @staticmethod
    def convert_to_alternative_login(login_list: FullName) -> FullName:
        return FullName(login_list.first_name, login_list.middle_name, login_list.last_name)

    @staticmethod
    def convert_to_reverse_login(login_list: FullName) -> FullName:
        return FullName(login_list.middle_name, login_list.first_name, login_list.last_name)



class PIH:

    version: str = "0.93"

    PATH: PATHS = PATHS

    class MC:

        @staticmethod
        def send_message(phone_number: str, message: str) -> bool:
            import pywhatkit as pwk
            try:
                pwk.sendwhatmsg_instantly(phone_number, message)
            except:
                pass

        def send_message_by_login(login: str, message: str) -> bool:
            user = ResultUnpack.unpack_first_data(
                PIH.RESULT.AD.user_by_login(login))
            if user is not None:
                PIH.MC.send_message(PIH.RESULT.EXTRACT.telephone(user), message)
            else:
                return False


    class RESULT:

        class EXTRACT:
    
            @staticmethod
            def parameter(data: dict, name: str) -> str:
                return data[name] if name in data else ""

            @staticmethod
            def tab_number(mark: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark, FIELD_NAME_COLLECTION.TAB_NUMBER)

            @staticmethod
            def telephone(user: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(user, FIELD_NAME_COLLECTION.TELEPHONE)

            @staticmethod
            def login(user: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(user, FIELD_NAME_COLLECTION.LOGIN)

            @staticmethod
            def name(mark: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark, FIELD_NAME_COLLECTION.NAME)

            @staticmethod
            def dn(user: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(user, FIELD_NAME_COLLECTION.DN)

            @staticmethod
            def as_full_name(mark: dict) -> FullName:
                return FullNameTool.from_string(PIH.RESULT.EXTRACT.parameter(mark, FIELD_NAME_COLLECTION.FULL_NAME))

            @staticmethod
            def full_name(mark: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark, FIELD_NAME_COLLECTION.FULL_NAME)

            @staticmethod
            def description(data: dict) -> str:
                result = PIH.RESULT.EXTRACT.parameter(data, FIELD_NAME_COLLECTION.DESCRIPTION)
                if isinstance(result, Tuple) or isinstance(result, List):
                    return result[0]

            @staticmethod
            def container_dn(user_data: dict) -> str:
                return ",".join(PIH.RESULT.EXTRACT.dn(user_data).split(",")[1:])
        
        class FILTER:

            def users_by_dn(data: List, dn: str) -> List:
                return list(filter(lambda x: PIH.RESULT.EXTRACT.container_dn(x).find(dn) != -1, data ))

        @staticmethod
        def represent(data: dict) -> str:
            return DataTools.represent(data)

        class ORION:

            @staticmethod
            def by_tab_number(value: str) -> dict:
                return DataTools.unrepresent(RPC_COMMANDS.ORION.get_mark_by_tab_number(value))

            @staticmethod
            def mark_by_person_name(value: str) -> dict:
                return DataTools.unrepresent(RPC_COMMANDS.ORION.get_mark_by_person_name(value))

            @staticmethod
            def free_marks() -> dict:
                return DataTools.unrepresent(RPC_COMMANDS.ORION.get_free_marks())

            @staticmethod
            def free_marks_by_group(group: Dict) -> dict:
                return DataTools.unrepresent(RPC_COMMANDS.ORION.get_free_marks_by_group(group))

            @staticmethod
            def free_marks_group_statistics() -> dict:
                return DataTools.unrepresent(RPC_COMMANDS.ORION.get_free_marks_group_statistics())

            @staticmethod
            def all_persons() -> dict:
                return DataTools.unrepresent(RPC_COMMANDS.ORION.get_all_persons())
        
        class AD:

            @staticmethod
            def user_by_login(value: str) -> dict:
                return DataTools.unrepresent(RPC_COMMANDS.AD.get_user_by_login(value))

            @staticmethod
            def templated_users() -> dict:
                return DataTools.unrepresent(RPC_COMMANDS.AD.get_templated_users())

            @staticmethod
            def containers() -> dict:
                return DataTools.unrepresent(RPC_COMMANDS.AD.get_containers())

            @staticmethod
            def by_full_name(value: FullName) -> dict:
                return DataTools.unrepresent(RPC_COMMANDS.AD.get_user_by_full_name(value))

            @staticmethod
            def by_name(value: str) -> dict:
                return DataTools.unrepresent(RPC_COMMANDS.AD.get_user_by_name(value))


    class COMBINE:

        @staticmethod
        def user_by_tab_number(value: str) -> dict:
            mard_data = ResultUnpack.unpack_first_data(PIH.RESULT.ORION.by_tab_number(value))
            if mard_data is not None:
                return ResultUnpack.unpack_first_data(PIH.RESULT.AD.by_full_name(PIH.RESULT.EXTRACT.as_full_name(mard_data)))
            return None


    class INPUT:

        @staticmethod
        def input(caption: str = None) -> str:
            try:
                return input() if caption is None else input(caption)
            except KeyboardInterrupt: 
                raise KeyboardInterrupt()

        @staticmethod
        def telephone() -> str:
            while True:
                PR.cyan("Telephone number:")
                telehone = PIH.INPUT.input()
                if PIH.CHECK.telephone(telehone):
                    return telehone
                else:
                    PR.red("Wrong telephone format!")

        @staticmethod
        def email() -> str:
            while True:
                PR.cyan("Email:")
                email = PIH.INPUT.input()
                if PIH.CHECK.email(email):
                    return email
                else:
                    PR.red("Wrong email format!")

        @staticmethod
        def description() -> str:
            PR.cyan("Description:")
            return PIH.INPUT.input()

        @staticmethod
        def login():
            while True:
                login = PIH.INPUT.input("Enter login:")
                if PIH.CHECK.login(login):
                    return login
                else:
                    PR.red("Wrong logib format")

        @staticmethod
        def indexed_field_list(list: FieldItemList, caption: str) -> str:
            for index, item in enumerate(list.list):
                print(f"{index + 1}: {item.caption}")
            name_list = list.get_name_list()
            return PIH.INPUT.item_by_index(caption, name_list)

        @staticmethod
        def index(caption: str, length: int, pre_action: Callable = None) -> int:
            selected_index = -1
            while True:
                if pre_action is not None:
                    pre_action()
                if length == 1:
                    return 0
                selected_index = PIH.INPUT.input(PR.green_str(caption + f" (from 1 to {length}):", "", " "))
                if selected_index == "":
                    selected_index = 1
                try:
                    selected_index = int(selected_index) - 1
                    if selected_index >= 0 and selected_index < length:
                        return selected_index
                except ValueError:
                    continue
        
        @staticmethod
        def item_by_index(caption: str, data: dict, pre_action: Callable = None) -> dict:
            return data[PIH.INPUT.index(caption, len(data), pre_action)]
               
               
        @staticmethod
        def tab_number(check: bool = True) -> str:
            tab_number: str = None
            while True:
                PR.green("Enter tab number:")
                tab_number = PIH.INPUT.input()
                if check:
                    if PIH.CHECK.tab_number(tab_number):
                        return tab_number
                    else:
                        PR.red("Wrong tab number")
                        return tab_number
                else:
                    return tab_number
                        

        @staticmethod
        def password(secret: bool = True, check: bool = False, settings: PasswordSettings = None) -> str:
            PR.cyan("Set password:")
            while True:
                value = getpass(" ") if secret else PIH.INPUT.input()
                if not check:
                    return value
                elif PIH.CHECK.password(value, settings):
                    return value
                else:
                    PR.red("Password not pass checking")

        @staticmethod
        def same_if_empty(caption: str, src_value: str) -> str:
            value = PIH.INPUT.input(caption)
            if value == "":
                value = src_value
            return value

        @staticmethod
        def name() -> str:
            PR.green("Enter part of name:")
            return PIH.INPUT.input()

        @staticmethod
        def full_name() -> FullName:
            full_name: FullName = FullName()
            while(True):
                last_name: str = PIH.INPUT.input("Введите фамилию:")
                last_name = last_name.strip()
                if PIH.CHECK.name_length(last_name):
                    full_name.last_name = last_name
                    break
                else:
                    pass
            while(True):
                first_name: str = PIH.INPUT.input("Введите имя:")
                first_name = first_name.strip()
                if PIH.CHECK.name_length(first_name):
                    full_name.first_name = first_name
                    break
                else:
                    pass
            while(True):
                middle_name: str = PIH.INPUT.input("Введите отчество:")
                middle_name = middle_name.strip()
                if PIH.CHECK.name_length(middle_name):
                    full_name.middle_name = middle_name
                    break
                else:
                    pass
            return full_name

        @staticmethod
        def templated_user() -> dict:
            result = PIH.RESULT.AD.templated_users()
            data = ResultUnpack.unpack_data(result)
            PIH.VISUAL.templated_users_for_result(result, True)
            return PIH.INPUT.item_by_index("Choose templated user:", data)

        def container() -> dict:
            result = PIH.RESULT.AD.containers()
            data = ResultUnpack.unpack_data(result)
            PIH.VISUAL.containers_for_result(result, True)
            return PIH.INPUT.item_by_index("Choose container by enter index", data)


        @staticmethod
        def yes_no(text: str = " ", enter_for_yes: bool = False) -> bool:
            answer = PIH.INPUT.input(f"{PR.blue_str(text)}{' ' if text != '' else ''}{PR.green_str(' Yes (Yes|Y|1|Enter) ')} {PR.red_str(' No (Another) ')}:" if enter_for_yes else
                           f"{PR.blue_str(text)}{' ' if text != '' else ''}{PR.red_str(' Yes (Yes|Y|1) ')} {PR.green_str(' No (Enter|Another) ')}:")
            answer = answer.lower()
            return answer == "y" or answer == "yes" or answer == "1" or (answer == "" and enter_for_yes)

        @staticmethod
        def free_mark() -> dict:
            group: dict = None
            while True:
                if PIH.INPUT.yes_no("Select group for free mark by search person's group by person name?"):
                    result = PIH.RESULT.ORION.mark_by_person_name(
                        PIH.INPUT.name())
                    data = ResultUnpack.unpack_data(result)
                    length = len(data)
                    if length > 0:
                        if length > 1:
                            PIH.VISUAL.table_with_caption_first_title_is_centered(result, "Search by name: ", True)
                        group = PIH.INPUT.item_by_index(
                            "Choose group by enter index", data)
                    else:
                        PR.red("No person with enterd name")
                else:
                    result = PIH.RESULT.ORION.free_marks_group_statistics()
                    data = ResultUnpack.unpack_data(result)
                    length = len(data)
                    if length > 0:
                        if length > 1:
                            PIH.VISUAL.free_marks_group_statistics_for_result(
                            result, True)
                        group = PIH.INPUT.item_by_index(
                            "Choose group by enter index", data)
                    else:
                        PR.red("No free marks!")
                        return None
                if group is not None: 
                    result = PIH.RESULT.ORION.free_marks_by_group(group)
                    data = ResultUnpack.unpack_data(result)
                    length = len(data)
                    if length > 0:
                        if length > 1:
                            PIH.VISUAL.free_marks_by_group_for_result(
                                group, result, True)
                        return PIH.INPUT.item_by_index(
                            "Choose mark by enter index", data)
                    else:
                        PR.red(f"No free marks for group {group[FIELD_NAME_COLLECTION.GROUP_NAME]}!")
                else:
                    pass

        @staticmethod
        def message_for_user_by_login(login: str) -> str:
            user = ResultUnpack.unpack_first_data(
                PIH.RESULT.AD.user_by_login(login))
            if user is not None:
                head_string = f"Здравствуйте, {PIH.RESULT.EXTRACT.name(user)}, "
                PR.green(head_string)
                message = PIH.INPUT.input(PR.blue_str("Enter message: "))
                return head_string + message
            else:
                pass

        @staticmethod
        def container_dn_or_templated_user_container_dn() -> str:
            container_type = PIH.INPUT.indexed_field_list(
                FIELD_COLLECTION.AD.CONTAINER_TYPE, "Choose type of container:")
            if container_type == FIELD_NAME_COLLECTION.TEMPLATE_USER_CONTAINER:
                return PIH.RESULT.EXTRACT.container_dn(PIH.INPUT.templated_user())
            else:
                return PIH.RESULT.EXTRACT.dn(PIH.INPUT.container())

    class CHECK:

        @staticmethod
        def user_is_exsits_by_login(value: str) -> bool:
            return RPC_COMMANDS.AD.user_is_exsits_by_login(value)

        @staticmethod
        def tab_number(value: str) -> bool:
            return re.fullmatch(r"[0-9]+", value) is not None

        @staticmethod
        def login(value: str) -> bool:
            pattern = r"([a-z]{"+ str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",}[0-9]*)"
            return re.fullmatch(pattern, value) is not None

        @staticmethod
        def telephone(value: str) -> bool:
            return re.fullmatch(r"^\+[0-9]{11,13}$", value) is not None

        @staticmethod
        def email(value: str) -> bool:
            return re.fullmatch(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", value) is not None

        @staticmethod
        def name_length(value: str) -> bool:
            return len(value) >= CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH

        @staticmethod
        def password(value: str, settings: PasswordSettings = None) -> bool:
            settings = settings or PASSWORD.SETTINGS.DEFAULT
            return PasswordTools.check_password(value, settings.length, settings.special_characters)

        def ping(host: str) -> bool:
            command = ['ping', "-n", '1', host]
            response = subprocess.call(command)
            return response == 0

    class VISUAL:

        @staticmethod
        def init() -> None:
            PR.init()

        @staticmethod
        def facade_header() -> None:
            PR.cyan("█▀█ ▄▀█ █▀▀ █ █▀▀ █ █▀▀   █ █▄░█ ▀█▀ █▀▀ █▀█ █▄░█ ▄▀█ ▀█▀ █ █▀█ █▄░█ ▄▀█ █░░   █░█ █▀█ █▀ █▀█ █ ▀█▀ ▄▀█ █░░")
            PR.cyan("█▀▀ █▀█ █▄▄ █ █▀░ █ █▄▄   █ █░▀█ ░█░ ██▄ █▀▄ █░▀█ █▀█ ░█░ █ █▄█ █░▀█ █▀█ █▄▄   █▀█ █▄█ ▄█ █▀▀ █ ░█░ █▀█ █▄▄")
            print(f"Version: {PIH.version}")

        @staticmethod
        def rpc_server_header(server_host: str, server_name: str) -> None:
            PR.blue("PIH")
            PR.blue(f"Version: {PIH.version}")
            PR.green(f"Server host: {server_host}")
            PR.green(f"Server name: {server_name}")

        @staticmethod
        def free_marks(use_index: bool = False) -> None:
            PIH.VISUAL.table_with_caption_first_title_is_centered(
                PIH.RESULT.ORION.free_marks(), "Free marks:", use_index)

        @staticmethod
        def mark_by_tab_number(value: str) -> None:
            PIH.VISUAL.mark_by_tab_number_for_result(PIH.RESULT.ORION.by_tab_number(value))

        @staticmethod
        def mark_by_tab_number_for_result(result: dict) -> None:
            PIH.VISUAL.table_with_caption_first_title_is_centered(
                result, "Mark by tab number:")

        @staticmethod
        def free_marks_group_statistics(use_index: bool = False) -> None:
            PIH.VISUAL.free_marks_group_statistics_for_result(
                PIH.RESULT.ORION.free_marks_group_statistics(), use_index)

        @staticmethod
        def free_marks_by_group(group: dict, use_index: bool = False) -> None:
            PIH.VISUAL.free_marks_by_group_for_result(
                PIH.RESULT.ORION.free_marks_by_group(group), group, use_index)

        @staticmethod
        def free_marks_group_statistics_for_result(result: dict, use_index: bool) -> None:
            PIH.VISUAL.table_with_caption_last_title_is_centered(result, "Free mark group statistics:", use_index)

        @staticmethod
        def free_marks_by_group_for_result(result: dict, group: dict, use_index: bool) -> None:
            group_name = group[FIELD_NAME_COLLECTION.GROUP_NAME]
            PIH.VISUAL.table_with_caption_last_title_is_centered(
                result, f"Free mark for group {group_name}:", use_index)

        @staticmethod
        def containers_for_result(result: dict, use_index: bool = False) -> None:
            PIH.VISUAL.table_with_caption(result, "Containers:", use_index)

        @staticmethod
        def table_with_caption_first_title_is_centered(data: Dict, caption: str, use_index: bool = False, modify_data_handler: Callable = None) -> None:
            def modify_table(table: PrettyTable, caption_list: List[str]):
                table.align[caption_list[int(use_index)]] = "c"
            PIH.VISUAL.table_with_caption(
                data, caption, use_index, modify_table, modify_data_handler)


        @staticmethod
        def table_with_caption_last_title_is_centered(data: dict, caption: str, use_index: bool = False, modify_data_handler: Callable = None) -> None:
            def modify_table(table: PrettyTable, caption_list: List[str]):
                table.align[caption_list[-1]] = "c"
            PIH.VISUAL.table_with_caption(
                data, caption, use_index, modify_table, modify_data_handler)

        @staticmethod
        def table_with_caption(result: dict, caption: str = None, use_index: bool = False, modify_table_handler: Callable = None, modify_data_handler: Callable = None) -> None:
            if caption is not None:
                PR.cyan(caption)
            field_list, data = ResultUnpack.unpack(result)
            if not isinstance(data, list):
                data = [data]
            if use_index:
                field_list.list.insert(0, FIELD_COLLECTION.INDEX)
            caption_list: List = field_list.get_caption_list()
            def create_table(caption_list: List[str]) -> PrettyTable:
                table: PrettyTable = PrettyTable(caption_list)
                table.align = "l"
                if use_index:
                    table.align[caption_list[0]] = "c"
                return table
            table: PrettyTable = create_table(caption_list)
            if modify_table_handler is not None:
                modify_table_handler(table, caption_list)
            if len(data) == 0:
                PR.red("Not found!")
            else:
                for index, item in enumerate(data):
                    row_data = []
                    for field_item_obj in field_list.get_list():
                        field_item: FieldItem = field_item_obj
                        if field_item.name == FIELD_COLLECTION.INDEX.name:
                            row_data.append(str(index + 1))
                        elif field_item.visible and field_item.name in item:
                            if modify_data_handler is not None:
                                item_data = modify_data_handler(field_item, item)
                                row_data.append(
                                    item[field_item.name] if item_data is None else item_data)
                            else:
                                row_data.append(item[field_item.name])
                    table.add_row(row_data)
                print(table)

        @staticmethod
        def templated_users_for_result(data: dict, use_index: bool = False) -> None:
            def data_handler(field_item: FieldItem, item: Any) -> Any:
                filed_name = field_item.name
                if filed_name == FIELD_NAME_COLLECTION.DESCRIPTION:
                    return PIH.RESULT.EXTRACT.description(item)
                return None
            PIH.VISUAL.table_with_caption(data, "Templated users:",use_index, None, data_handler)

    class ACTION:

        class AD:

            @staticmethod
            def create_user_from_template(templated_user: dict,
                                      full_name: FullName, login: str, password : str, description: str, telephone: str, email: str) -> bool:
                return RPC_COMMANDS.AD.create_user_from_template(
                        PIH.RESULT.EXTRACT.dn(templated_user), full_name, login, password, description, telephone, email)


            @staticmethod
            def create_user_in_container(container: dict,
                                      full_name: FullName, login: str, password : str, description: str, telephone: str, email: str) -> bool:
                return RPC_COMMANDS.AD.create_user_in_container(
                        PIH.RESULT.EXTRACT.dn(container), full_name, login, password, description, telephone, email)
           
            @staticmethod
            def user_set_telephone(user: dict, telephone: str) -> bool:
                return RPC_COMMANDS.AD.user_set_telephone(PIH.RESULT.EXTRACT.dn(user), telephone)


        class ORION:

            @staticmethod
            def create_mark(full_name: FullName, tab_number: str) -> bool:
                return PIH.ACTION.ORION.update_full_name_by_tab_number(full_name, tab_number)

            @staticmethod
            def update_full_name_by_tab_number(full_name: FullName, tab_number: str) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.ORION.rename_person_by_tab_number(full_name, tab_number))

            @staticmethod
            def make_mark_as_free_by_tab_number(tab_number: str) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.ORION.make_mark_as_free_by_tab_number(tab_number))

        def create_user_documents(full_name: FullName, tab_number: str, pc: LoginPasswordPair, polibase: LoginPasswordPair, email: LoginPasswordPair) -> bool:
            locale.setlocale(locale.LC_ALL, 'ru_RU')
            date_now = datetime.now().date()
            date_now_string = f"{date_now.day} {calendar.month_name[date_now.month]} {date_now.year}"
            full_name_string = FullNameTool.to_string(full_name)
            return RPC_COMMANDS.TEMPLATE.create_user_documents(PIH.PATH.IT.NEW_EMPLOYERS(f"{full_name_string}.docx"), date_now_string, CONST.SITE, CONST.SITE_PROTOCOL + CONST.SITE, CONST.EMAIL_ADDRESS, full_name, tab_number, pc, polibase, email)
        

        def generate_login(full_name: FullName) -> str:
            login: FullName = NamePolicy.convert_to_login(full_name)
            login_string: str = FullNameTool.to_string(login)
            if PIH.CHECK.user_is_exsits_by_login(login_string):
                PR.red(f"Login '{login_string}' is not free")
                login_alt = NamePolicy.convert_to_alternative_login(
                    login)
                login_string = FullNameTool.to_string(login_alt)
                if PIH.CHECK.user_is_exsits_by_login(login_string):
                    PR.red(f"Login '{login_string}' is not free")
                    login_reversed = NamePolicy.convert_to_reverse_login(login)
                    login_string = FullNameTool.to_string(login_reversed)
                    if PIH.CHECK.user_is_exsits_by_login(login_string):
                        PR.red(f"Login '{login_string}' is not free")
                        while True:
                            login_string = PIH.INPUT.login()
                            if PIH.CHECK.user_is_exsits_by_login(login_string):
                                break
                            else:
                                PR.red(f"Login '{login_string}' is not free")
                        return None
            return login_string

        @staticmethod
        def generate_password(once: bool = False, settings: PasswordSettings = None) -> str:
            def generate_password_interanal(settings: PasswordSettings = None) -> str:
                settings = settings or PASSWORD.SETTINGS.DEFAULT
                return PasswordTools.generate_random_password(settings.length, settings.special_characters,
                settings.order_list, settings.special_characters_count, 
                settings.alphabets_lowercase_count, settings.alphabets_uppercase_count, 
                settings.digits_count, settings.shuffled)
            while True:  
                password = generate_password_interanal(settings)
                PR.green(f"{password}")
                if once or PIH.INPUT.yes_no("Use this password?", True):
                    return password
                else:
                    pass

        @staticmethod
        def generate_email(login: str) -> str:
            return "@".join([login, CONST.SITE])

class PR:

    @staticmethod
    def init() -> None:
        colorama.init()

    @staticmethod
    def color_str(color: int, string: str, before_text: str = "", after_text: str = "") -> str:
        return f"{before_text}{color}{string}{Back.RESET}{after_text}"

    @staticmethod
    def color(string: str) -> None:
        print(string)

    @staticmethod
    def green_str(string: str, before_text: str = "", after_text: str = "") -> str:
        return PR.color_str(Back.GREEN, string, before_text, after_text)

    @staticmethod
    def green(string: str, before_text: str = "", after_text: str = "") -> None:
        PR.color(PR.green_str(string, before_text, after_text))

    @staticmethod
    def yellow_str(string: str, before_text: str = "", after_text: str = "") -> str:
        return PR.color_str(Back.YELLOW, string, before_text, after_text)

    @staticmethod
    def yellow(string: str, before_text: str = "", after_text: str = "") -> None:
        PR.color(PR.yellow_str(string, before_text, after_text))

    @staticmethod
    def black_str(string: str, before_text: str = "", after_text: str = "") -> str:
        return PR.color_str(Back.BLACK, string, before_text, after_text)

    @staticmethod
    def black(string: str, before_text: str = "", after_text: str = "") -> None:
        PR.color(PR.black_str(string, before_text, after_text))

    @staticmethod
    def white_str(string: str, before_text: str = "", after_text: str = "") -> str:
        return PR.color_str(Back.WHITE, string, before_text, after_text)

    @staticmethod
    def white(string: str, before_text: str = "", after_text: str = "") -> None:
        PR.color(PR.white_str(string, before_text, after_text))

    @staticmethod
    def magenta_str(string: str, before_text: str = "", after_text: str = "") -> str:
        return PR.color_str(Back.MAGENTA, string, before_text, after_text)

    @staticmethod
    def magenta(string: str, before_text: str = "", after_text: str = "") -> None:
        PR.color(PR.magenta_str(string, before_text, after_text))

    @staticmethod
    def cyan(string: str, before_text: str = "", after_text: str = "") -> None:
        PR.color(PR.cyan_str(string, before_text, after_text))

    @staticmethod
    def cyan_str(string: str, before_text: str = "", after_text: str = "") -> str:
        return PR.color_str(Back.CYAN, string, before_text, after_text)

    @staticmethod
    def red(string: str, before_text: str = "", after_text: str = "") -> None:
        PR.color(PR.red_str(string, before_text, after_text))

    @staticmethod
    def red_str(string: str, before_text: str = "", after_text: str = "") -> str:
        return PR.color_str(Back.RED, string, before_text, after_text)

    @staticmethod
    def blue(string: str, before_text: str = "", after_text: str = "") -> None:
        PR.color(PR.blue_str(string, before_text, after_text))

    @staticmethod
    def blue_str(string: str, before_text: str = "", after_text: str = "") -> str:
        return PR.color_str(Back.BLUE, string, before_text, after_text)

    @staticmethod
    def bright(string: str, before_text: str = "", after_text: str = "") -> None:
        PR.color(PR.bright_str(string, before_text, after_text))

    @staticmethod
    def bright_str(string: str, before_text: str = "", after_text: str = "") -> str:
        return PR.color_str(Style.BRIGHT, string, before_text, after_text)
