from PyQt5 import QtWidgets
import yaml


class DashSettingConfig(object):
    def __init__(self, controller):
        self.controller = controller
        self.list_selection_view = ["left_window", "right_window", "driver", "second_driver", "original"]
        self.configuration_view = {}
        self.init_properties_config_view()
        self.connect()

    def connect(self):
        self.controller.spinBox_alpha_max_dash.valueChanged.connect(self.change_properties_panorama)
        self.controller.doubleSpinBox_alpha_dash.valueChanged.connect(self.change_properties_panorama)
        self.controller.doubleSpinBox_beta_dash.valueChanged.connect(self.change_properties_panorama)
        # self.controller.doubleSpinBox_alpha_from_dash.valueChanged.connect(self.change_properties_panorama)

        self.controller.doubleSpinBox_crop_left_dash.valueChanged.connect(self.change_properties_cropping_panorama)
        self.controller.doubleSpinBox_crop_right_dash.valueChanged.connect(self.change_properties_cropping_panorama)
        self.controller.doubleSpinBox_crop_top_dash.valueChanged.connect(self.change_properties_cropping_panorama)
        self.controller.doubleSpinBox_crop_bottom_dash.valueChanged.connect(self.change_properties_cropping_panorama)

        self.controller.spinBox_alpha_anypoint_view.valueChanged.connect(self.change_properties_anypoint)
        self.controller.spinBox_beta_anypoint_view.valueChanged.connect(self.change_properties_anypoint)
        self.controller.spinBox_roll_anypoint_view.valueChanged.connect(self.change_properties_anypoint)
        self.controller.spinBox_zoom_anypoint_view.valueChanged.connect(self.change_properties_anypoint)

        self.controller.spinBox_rotate_image_original.valueChanged.connect(self.change_rotate_original_image)

        self.controller.spinBox_alpha_front_view.valueChanged.connect(self.change_anypoint_mode_2)
        self.controller.spinBox_beta_front_view.valueChanged.connect(self.change_anypoint_mode_2)
        self.controller.spinBox_zoom_front_view.valueChanged.connect(self.change_anypoint_mode_2)
        self.controller.crop_top_anypoint_2.valueChanged.connect(self.change_anypoint_mode_2)
        self.controller.crop_bottom_anypoint_2.valueChanged.connect(self.change_anypoint_mode_2)

        self.controller.spinBox_alpha_max_panorama.valueChanged.connect(self.change_x_panorama)
        self.controller.spinBox_alpha_min_panorama.valueChanged.connect(self.change_x_panorama)
        self.controller.crop_top_x_panorama.valueChanged.connect(self.change_x_panorama)
        self.controller.crop_bottom_x_panorama.valueChanged.connect(self.change_x_panorama)

        self.controller.comboBox_select_view.currentIndexChanged.connect(self.change_anypoint_view)

        self.controller.btn_close_dash.clicked.connect(self.controller.onclick_close_setting_mode)

    def onclick_save_config(self):
        self.controller.model.save_config(self.controller.config_path)
        QtWidgets.QMessageBox.information(None, "Information!!", "Config saved!")

    def init_create_properties_config_view(self):
        """
        Use for create config file

        Returns:

        """
        for view in self.list_selection_view:
            print(view)

    def init_properties_config_view(self):
        with open(self.controller.source_file.get_configuration_view_file(), "r") as file:
            self.configuration_view = yaml.safe_load(file)
        self.controller.spinBox_alpha_anypoint_view.setValue(self.configuration_view["left_window"]["alpha"])
        self.controller.spinBox_beta_anypoint_view.setValue(self.configuration_view["left_window"]["beta"])
        self.controller.spinBox_roll_anypoint_view.setValue(self.configuration_view["left_window"]["roll"])
        self.controller.spinBox_zoom_anypoint_view.setValue(self.configuration_view["left_window"]["zoom"])

        self.controller.spinBox_alpha_max_dash.setValue(self.configuration_view["panorama"]["alpha_max"])
        self.controller.doubleSpinBox_alpha_dash.setValue(self.configuration_view["panorama"]["alpha"])
        self.controller.doubleSpinBox_beta_dash.setValue(self.configuration_view["panorama"]["beta"])
        # self.controller.doubleSpinBox_alpha_from_dash.setValue(self.configuration_view["panorama"]["alpha_from"])

        self.controller.doubleSpinBox_crop_left_dash.setValue(self.configuration_view["panorama"]["crop_left"])
        self.controller.doubleSpinBox_crop_right_dash.setValue(self.configuration_view["panorama"]["crop_right"])
        self.controller.doubleSpinBox_crop_top_dash.setValue(self.configuration_view["panorama"]["crop_top"])
        self.controller.doubleSpinBox_crop_bottom_dash.setValue(self.configuration_view["panorama"]["crop_bottom"])

        self.controller.spinBox_rotate_image_original.setValue(self.configuration_view["original"]["rotate"])

        self.controller.spinBox_alpha_front_view.setValue(self.configuration_view["anypoint_mode_2"]["alpha"])
        self.controller.spinBox_beta_front_view.setValue(self.configuration_view["anypoint_mode_2"]["beta"])
        self.controller.spinBox_zoom_front_view.setValue(self.configuration_view["anypoint_mode_2"]["zoom"])
        self.controller.crop_top_anypoint_2.setValue(self.configuration_view["anypoint_mode_2"]["crop_top"])
        self.controller.crop_bottom_anypoint_2.setValue(self.configuration_view["anypoint_mode_2"]["crop_bottom"])

        self.controller.spinBox_alpha_max_panorama.setValue(self.configuration_view["x_panorama"]["alpha_max"])
        self.controller.spinBox_alpha_min_panorama.setValue(self.configuration_view["x_panorama"]["alpha_min"])
        self.controller.crop_top_x_panorama.setValue(self.configuration_view["x_panorama"]["crop_top"])
        self.controller.crop_bottom_x_panorama.setValue(self.configuration_view["x_panorama"]["crop_bottom"])

    def change_properties_anypoint(self):
        view = self.list_selection_view[self.controller.comboBox_select_view.currentIndex()]
        self.configuration_view[view]["alpha"] = self.controller.spinBox_alpha_anypoint_view.value()
        self.configuration_view[view]["beta"] = self.controller.spinBox_beta_anypoint_view.value()
        self.configuration_view[view]["roll"] = self.controller.spinBox_roll_anypoint_view.value()
        self.configuration_view[view]["zoom"] = self.controller.spinBox_zoom_anypoint_view.value()

        if self.controller.model.image is not None:
            with open(self.controller.source_file.get_configuration_view_file(), "w") as outfile:
                yaml.dump(self.configuration_view, outfile, default_flow_style=False)
            self.controller.model.create_maps_anypoint_view(view)
            self.controller.showing_image_to_ui()

    def change_anypoint_view(self):
        view = self.list_selection_view[self.controller.comboBox_select_view.currentIndex()]
        self.block_signal()
        with open(self.controller.source_file.get_configuration_view_file(), "r") as file:
            data = yaml.safe_load(file)
        self.controller.spinBox_alpha_anypoint_view.setValue(data[view]["alpha"])
        self.controller.spinBox_beta_anypoint_view.setValue(data[view]["beta"])
        self.controller.spinBox_roll_anypoint_view.setValue(data[view]["roll"])
        self.controller.spinBox_zoom_anypoint_view.setValue(data[view]["zoom"])
        self.unblock_signal()
        self.controller.showing_image_to_ui()

    def change_properties_panorama(self):
        self.configuration_view["panorama"]["alpha_max"] = self.controller.spinBox_alpha_max_dash.value()
        self.configuration_view["panorama"]["alpha"] = self.controller.doubleSpinBox_alpha_dash.value()
        self.configuration_view["panorama"]["beta"] = self.controller.doubleSpinBox_beta_dash.value()
        # self.configuration_view["panorama"]["alpha_from"] = self.controller.doubleSpinBox_alpha_from_dash.value()
        if self.controller.model.image is not None:
            with open(self.controller.source_file.get_configuration_view_file(), "w") as outfile:
                yaml.dump(self.configuration_view, outfile, default_flow_style=False)
            self.controller.model.create_maps_panorama_dash()
            self.controller.showing_image_to_ui()

    def change_anypoint_mode_2(self):
        self.configuration_view["anypoint_mode_2"]["alpha"] = self.controller.spinBox_alpha_front_view.value()
        self.configuration_view["anypoint_mode_2"]["beta"] = self.controller.spinBox_beta_front_view.value()
        self.configuration_view["anypoint_mode_2"]["zoom"] = self.controller.spinBox_zoom_front_view.value()
        self.configuration_view["anypoint_mode_2"]["crop_top"] = self.controller.crop_top_anypoint_2.value()
        if self.controller.crop_bottom_anypoint_2.value() > self.controller.crop_top_anypoint_2.value() + 0.2:
            self.configuration_view["anypoint_mode_2"]["crop_bottom"] = self.controller.crop_bottom_anypoint_2.value()
        if self.controller.model.image is not None:
            with open(self.controller.source_file.get_configuration_view_file(), "w") as outfile:
                yaml.dump(self.configuration_view, outfile, default_flow_style=False)
            self.controller.model.create_maps_anypoint_mode_2()
            self.controller.showing_image_to_ui()

    def change_x_panorama(self):
        self.configuration_view["x_panorama"]["alpha_max"] = self.controller.spinBox_alpha_max_panorama.value()
        self.configuration_view["x_panorama"]["alpha_min"] = self.controller.spinBox_alpha_min_panorama.value()
        self.configuration_view["x_panorama"]["crop_top"] = self.controller.crop_top_x_panorama.value()
        if self.controller.crop_bottom_x_panorama.value() > self.controller.crop_top_x_panorama.value() + 0.2:
            self.configuration_view["x_panorama"]["crop_bottom"] = self.controller.crop_bottom_x_panorama.value()
        if self.controller.model.image is not None:
            with open(self.controller.source_file.get_configuration_view_file(), "w") as outfile:
                yaml.dump(self.configuration_view, outfile, default_flow_style=False)
            self.controller.model.create_maps_panorama_x()
            self.controller.showing_image_to_ui()

    def change_properties_cropping_panorama(self):
        self.configuration_view["panorama"]["crop_left"] = self.controller.doubleSpinBox_crop_left_dash.value()
        if self.controller.doubleSpinBox_crop_right_dash.value() > self.controller.doubleSpinBox_crop_left_dash.value() + 0.2:
            self.configuration_view["panorama"]["crop_right"] = self.controller.doubleSpinBox_crop_right_dash.value()
        self.configuration_view["panorama"]["crop_top"] = self.controller.doubleSpinBox_crop_top_dash.value()
        if self.controller.doubleSpinBox_crop_bottom_dash.value() > self.controller.doubleSpinBox_crop_top_dash.value() + 0.2:
            self.configuration_view["panorama"]["crop_bottom"] = self.controller.doubleSpinBox_crop_bottom_dash.value()
        with open(self.controller.source_file.get_configuration_view_file(), "w") as outfile:
            yaml.dump(self.configuration_view, outfile, default_flow_style=False)
        self.controller.showing_image_to_ui()

    def change_rotate_original_image(self):
        self.configuration_view["original"]["rotate"] = self.controller.spinBox_rotate_image_original.value()
        with open(self.controller.source_file.get_configuration_view_file(), "w") as outfile:
            yaml.dump(self.configuration_view, outfile, default_flow_style=False)
        self.controller.model.set_rotation_angle_ori()
        self.controller.showing_image_to_ui()

    def block_signal(self):
        self.controller.spinBox_alpha_max_dash.blockSignals(True)
        self.controller.doubleSpinBox_alpha_dash.blockSignals(True)
        self.controller.doubleSpinBox_beta_dash.blockSignals(True)
        # self.controller.doubleSpinBox_alpha_from_dash.blockSignals(True)

        self.controller.spinBox_alpha_anypoint_view.blockSignals(True)
        self.controller.spinBox_beta_anypoint_view.blockSignals(True)
        self.controller.spinBox_zoom_anypoint_view.blockSignals(True)
        # self.controller.doubleSpinBox_crop_view.blockSignals(True)

        self.controller.doubleSpinBox_crop_left_dash.blockSignals(True)
        self.controller.doubleSpinBox_crop_right_dash.blockSignals(True)
        self.controller.doubleSpinBox_crop_top_dash.blockSignals(True)
        self.controller.doubleSpinBox_crop_bottom_dash.blockSignals(True)

    def unblock_signal(self):
        self.controller.spinBox_alpha_max_dash.blockSignals(False)
        self.controller.doubleSpinBox_alpha_dash.blockSignals(False)
        self.controller.doubleSpinBox_beta_dash.blockSignals(False)
        # self.controller.doubleSpinBox_alpha_from_dash.blockSignals(False)

        self.controller.spinBox_alpha_anypoint_view.blockSignals(False)
        self.controller.spinBox_beta_anypoint_view.blockSignals(False)
        self.controller.spinBox_zoom_anypoint_view.blockSignals(False)
        # self.controller.doubleSpinBox_crop_view.blockSignals(False)

        self.controller.doubleSpinBox_crop_left_dash.blockSignals(False)
        self.controller.doubleSpinBox_crop_right_dash.blockSignals(False)
        self.controller.doubleSpinBox_crop_top_dash.blockSignals(False)
        self.controller.doubleSpinBox_crop_bottom_dash.blockSignals(False)
