#include "climate.h"

namespace esphome {
namespace otgw {

static const char *const TAG = "otgw.climate";
static const float NaN = std::numeric_limits<float>::quiet_NaN();

static const uint8_t DATA_ID_STATUS = 0;
static const uint8_t DATA_ID_ROOM_SETPOINT = 16;
static const uint8_t DATA_ID_ROOM_TEMPERATURE = 24;

void OpenThermGatewayClimateThermostat::setup() {
    this->mode = climate::CLIMATE_MODE_OFF;
    this->action = climate::CLIMATE_ACTION_OFF;

    auto listener = [this](const OpenThermMessage &message) { this->on_otmessage(message); };
    this->parent_->register_listener(DATA_ID_STATUS, listener);
    this->parent_->register_listener(DATA_ID_ROOM_SETPOINT, listener);
    this->parent_->register_listener(DATA_ID_ROOM_TEMPERATURE, listener);

    this->parent_->register_timeout_listener([this]() { this->on_timeout(); });
}

void OpenThermGatewayClimateThermostat::dump_config() {
    LOG_CLIMATE("", "OpenTherm Gateway Climate", this);
    if (this->target_temperature_constant_) {
        ESP_LOGCONFIG(TAG, "  Target Temperature is set Constant");
    } else {
        ESP_LOGCONFIG(TAG, "  Target Temperature is set Temporary");
    }
    if (this->external_sensor_) {
        ESP_LOGCONFIG(TAG, "  Using external temperature sensor: %s", this->external_sensor_->get_name().c_str());
    }
}

void OpenThermGatewayClimateThermostat::control(const climate::ClimateCall& call) {
    if (call.get_target_temperature().has_value()) {
        this->target_temperature = *call.get_target_temperature();
        this->parent_->set_room_temperature(this->target_temperature, this->target_temperature_constant_);
        this->publish_state();
    }
}

void OpenThermGatewayClimateThermostat::on_otmessage(const OpenThermMessage &message) {
    switch (message.data_id) {
        case DATA_ID_STATUS: {
            bool ch1_active = (message.value_u16 >> 1) & 1;
            bool ch2_active = (message.value_u16 >> 5) & 1;
            bool cooling_active = (message.value_u16 >> 4) & 1;

            if (ch1_active || ch2_active) {
                this->mode = climate::CLIMATE_MODE_HEAT;
                this->action = climate::CLIMATE_ACTION_HEATING;
            } else if (cooling_active) {
                this->mode = climate::CLIMATE_MODE_COOL;
                this->action = climate::CLIMATE_ACTION_COOLING;
            } else {
                this->mode = climate::CLIMATE_MODE_HEAT;
                this->action = climate::CLIMATE_ACTION_IDLE;
            }
            break;
        }
        case DATA_ID_ROOM_SETPOINT:
            this->target_temperature = message.value_f88;
            break;
        case DATA_ID_ROOM_TEMPERATURE:
            if (!this->external_sensor_) {
                this->current_temperature = message.value_f88;
            }
            break;
    }

    // override with external sensor if configured
    if (this->external_sensor_) {
        this->current_temperature = this->external_sensor_->state;
    }

    this->publish_state();
}

void OpenThermGatewayClimateThermostat::on_timeout() {
    this->target_temperature = NaN;
    this->current_temperature = NaN;
    this->mode = climate::CLIMATE_MODE_OFF;
    this->action = climate::CLIMATE_ACTION_OFF;
    this->publish_state();
}

climate::ClimateTraits OpenThermGatewayClimateThermostat::traits() {
    auto traits = climate::ClimateTraits();
    traits.set_supports_action(true);
    traits.set_supports_current_temperature(true);
    traits.set_supported_modes({});

    traits.set_visual_min_temperature(1);
    traits.set_visual_max_temperature(30);
    traits.set_visual_temperature_step(0.1);
    traits.set_visual_target_temperature_step(0.5);

    return traits;
}

}  // namespace otgw
}  // namespace esphome
