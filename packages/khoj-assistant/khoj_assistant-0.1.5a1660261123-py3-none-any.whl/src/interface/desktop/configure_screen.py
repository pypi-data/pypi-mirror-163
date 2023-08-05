# Standard Packages
from pathlib import Path

# External Packages
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

# Internal Packages
from src.configure import configure_server
from src.interface.desktop.file_browser import FileBrowser
from src.utils import constants, state, yaml as yaml_utils
from src.utils.cli import cli
from src.utils.config import SearchType, ProcessorType
from src.utils.helpers import merge_dicts, resolve_absolute_path


class ConfigureScreen(QtWidgets.QDialog):
    """Create Window to Configure Khoj
    Allow user to
    1. Configure content types to search
    2. Configure conversation processor
    3. Save the configuration to khoj.yml
    """

    def __init__(self, config_file: Path, parent=None):
        super(ConfigureScreen, self).__init__(parent=parent)
        self.config_file = config_file

        # Load config from existing config, if exists, else load from default config
        if resolve_absolute_path(self.config_file).exists():
            self.current_config = yaml_utils.load_config_from_file(self.config_file)
        else:
            self.current_config = constants.default_config
        self.new_config = self.current_config

        # Initialize Configure Window
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("Khoj - Configure")

        # Initialize Configure Window Layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Add Settings Panels for each Search Type to Configure Window Layout
        self.search_settings_panels = []
        for search_type in SearchType:
            current_content_config = self.current_config['content-type'].get(search_type, {})
            self.search_settings_panels += [self.add_settings_panel(current_content_config, search_type, layout)]

        # Add Conversation Processor Panel to Configure Screen
        self.processor_settings_panels = []
        conversation_type = ProcessorType.Conversation
        current_conversation_config = self.current_config['processor'].get(conversation_type, {})
        self.processor_settings_panels += [self.add_processor_panel(current_conversation_config, conversation_type, layout)]

        self.add_action_panel(layout)

    def add_settings_panel(self, current_content_config: dict, search_type: SearchType, parent_layout: QtWidgets.QLayout):
        "Add Settings Panel for specified Search Type. Toggle Editable Search Types"
        # Get current files from config for given search type
        if search_type == SearchType.Image:
            current_content_files = current_content_config.get('input-directories', [])
            file_input_text = f'{search_type.name} Folders'
        else:
            current_content_files = current_content_config.get('input-files', [])
            file_input_text = f'{search_type.name} Files'

        # Create widgets to display settings for given search type
        search_type_settings = QtWidgets.QWidget()
        search_type_layout = QtWidgets.QVBoxLayout(search_type_settings)
        enable_search_type = SearchCheckBox(f"Search {search_type.name}", search_type)
        # Add file browser to set input files for given search type
        input_files = FileBrowser(file_input_text, search_type, current_content_files)

        # Set enabled/disabled based on checkbox state
        enable_search_type.setChecked(current_content_files is not None and len(current_content_files) > 0)
        input_files.setEnabled(enable_search_type.isChecked())
        enable_search_type.stateChanged.connect(lambda _: input_files.setEnabled(enable_search_type.isChecked()))

        # Add setting widgets for given search type to panel
        search_type_layout.addWidget(enable_search_type)
        search_type_layout.addWidget(input_files)
        parent_layout.addWidget(search_type_settings)

        return search_type_settings

    def add_processor_panel(self, current_conversation_config: dict, processor_type: ProcessorType, parent_layout: QtWidgets.QLayout):
        "Add Conversation Processor Panel"
        current_openai_api_key = current_conversation_config.get('openai-api-key', None)
        processor_type_settings = QtWidgets.QWidget()
        processor_type_layout = QtWidgets.QVBoxLayout(processor_type_settings)

        enable_conversation = ProcessorCheckBox(f"Conversation", processor_type)
        enable_conversation.setChecked(current_openai_api_key is not None)

        conversation_settings = QtWidgets.QWidget()
        conversation_settings_layout = QtWidgets.QHBoxLayout(conversation_settings)
        input_label = QtWidgets.QLabel()
        input_label.setText("OpenAI API Key")
        input_label.setFixedWidth(95)

        input_field = ProcessorLineEdit(current_openai_api_key, processor_type)
        input_field.setFixedWidth(245)

        input_field.setEnabled(enable_conversation.isChecked())
        enable_conversation.stateChanged.connect(lambda _: input_field.setEnabled(enable_conversation.isChecked()))

        conversation_settings_layout.addWidget(input_label)
        conversation_settings_layout.addWidget(input_field)

        processor_type_layout.addWidget(enable_conversation)
        processor_type_layout.addWidget(conversation_settings)

        parent_layout.addWidget(processor_type_settings)
        return processor_type_settings

    def add_action_panel(self, parent_layout: QtWidgets.QLayout):
        "Add Action Panel"
        # Button to Save Settings
        action_bar = QtWidgets.QWidget()
        action_bar_layout = QtWidgets.QHBoxLayout(action_bar)

        save_button = QtWidgets.QPushButton("Start", clicked=self.save_settings)

        action_bar_layout.addWidget(save_button)
        parent_layout.addWidget(action_bar)

    def get_default_config(self, search_type:SearchType=None, processor_type:ProcessorType=None):
        "Get default config"
        config = constants.default_config
        if search_type:
            return config['content-type'][search_type]
        elif processor_type:
            return config['processor'][processor_type]
        else:
            return config

    def add_error_message(self, message: str, parent_layout: QtWidgets.QLayout):
        "Add Error Message to Configure Screen"
        error_message = QtWidgets.QLabel()
        error_message.setWordWrap(True)
        error_message.setText(message)
        error_message.setStyleSheet("color: red")
        parent_layout.addWidget(error_message)

    def update_search_settings(self):
        "Update config with search settings from UI"
        for settings_panel in self.search_settings_panels:
            for child in settings_panel.children():
                if not isinstance(child, (SearchCheckBox, FileBrowser)):
                    continue
                if isinstance(child, SearchCheckBox):
                    # Search Type Disabled
                    if not child.isChecked() and child.search_type in self.new_config['content-type']:
                        del self.new_config['content-type'][child.search_type]
                    # Search Type (re)-Enabled
                    if child.isChecked():
                        current_search_config = self.current_config['content-type'].get(child.search_type, {})
                        default_search_config = self.get_default_config(search_type = child.search_type)
                        self.new_config['content-type'][child.search_type.value] = merge_dicts(current_search_config, default_search_config)
                elif isinstance(child, FileBrowser) and child.search_type in self.new_config['content-type']:
                    self.new_config['content-type'][child.search_type.value]['input-files'] = child.getPaths() if child.getPaths() != [] else None

    def update_processor_settings(self):
        "Update config with conversation settings from UI"
        for settings_panel in self.processor_settings_panels:
            for child in settings_panel.children():
                if isinstance(child, QtWidgets.QWidget) and child.findChild(ProcessorLineEdit):
                    child = child.findChild(ProcessorLineEdit)
                elif not isinstance(child, ProcessorCheckBox):
                    continue
                if isinstance(child, ProcessorCheckBox):
                    # Processor Type Disabled
                    if not child.isChecked() and child.processor_type in self.new_config['processor']:
                        del self.new_config['processor'][child.processor_type]
                    # Processor Type (re)-Enabled
                    if child.isChecked():
                        current_processor_config = self.current_config['processor'].get(child.processor_type, {})
                        default_processor_config = self.get_default_config(processor_type = child.processor_type)
                        self.new_config['processor'][child.processor_type.value] = merge_dicts(current_processor_config, default_processor_config)
                elif isinstance(child, ProcessorLineEdit) and child.processor_type in self.new_config['processor']:
                    if child.processor_type == ProcessorType.Conversation:
                        self.new_config['processor'][child.processor_type.value]['openai-api-key'] = child.text() if child.text() != '' else None

    def save_settings_to_file(self) -> bool:
        # Validate config before writing to file
        try:
            yaml_utils.parse_config_from_string(self.new_config)
        except Exception as e:
            print(f"Error validating config: {e}")
            self.add_error_message(f"Error validating config: {e}", self.layout())
            return False
        else:
            # Remove error message if present
            for i in range(self.layout().count()):
                current_widget = self.layout().itemAt(i).widget()
                if isinstance(current_widget, QtWidgets.QLabel) and current_widget.text().startswith("Error validating config:"):
                    self.layout().removeWidget(current_widget)
                    current_widget.deleteLater()

        # Save the config to app config file
        yaml_utils.save_config_to_file(self.new_config, self.config_file)
        return True

    def load_updated_settings(self):
        "Hot swap to use the updated config from config file"
        # Load parsed, validated config from app config file
        args = cli(state.cli_args)
        self.current_config = self.new_config

        # Configure server with loaded config
        configure_server(args, required=True)

    def save_settings(self):
        "Save the settings to khoj.yml"
        self.update_search_settings()
        self.update_processor_settings()
        if self.save_settings_to_file():
            self.load_updated_settings()
            self.hide()


class SearchCheckBox(QtWidgets.QCheckBox):
    def __init__(self, text, search_type: SearchType, parent=None):
        self.search_type = search_type
        super(SearchCheckBox, self).__init__(text, parent=parent)


class ProcessorCheckBox(QtWidgets.QCheckBox):
    def __init__(self, text, processor_type: ProcessorType, parent=None):
        self.processor_type = processor_type
        super(ProcessorCheckBox, self).__init__(text, parent=parent)


class ProcessorLineEdit(QtWidgets.QLineEdit):
    def __init__(self, text, processor_type: ProcessorType, parent=None):
        self.processor_type = processor_type
        if text is None:
            super(ProcessorLineEdit, self).__init__(parent=parent)
        else:
            super(ProcessorLineEdit, self).__init__(text, parent=parent)
