#pragma once

#include "esphome/core/component.h"
#include "esphome/components/climate/climate.h"
#include "esphome/components/otgw/otgw.h"
#include "esphome/components/sensor/sensor.h"

namespace esphome {
namespace otgw {

enum class RoomTemperatureSource {
  OTGW_THERMOSTAT,
  EXTERNAL_SENSOR,
};

class OpenThermGatewayClimateThermostat : public climate::Climate, public Component {
  public:
    void setup() override;
    void dump_config() override;
    climate::ClimateTraits traits() override;
    void control(const climate::ClimateCall& call) override;
    void loop() override;  // nodig om externe sensor elke cycle te lezen

    void set_parent(OpenThermGateway *parent) { this->parent_ = parent; }
    void set_target_temperature_constant(bool constant) { this->target_temperature_constant_ = constant; }

    void set_room_temperature_source(RoomTemperatureSource src) { this->room_temp_source_ = src; }
    void set_external_room_sensor(sensor::Sensor *sensor) { this->external_room_sensor_ = sensor; }

  protected:
    OpenThermGateway *parent_;
    bool target_temperature_constant_;

    void on_otmessage(const OpenThermMessage &message);
    void on_timeout();

    RoomTemperatureSource room_temp_source_{RoomTemperatureSource::OTGW_THERMOSTAT};
    sensor::Sensor *external_room_sensor_{nullptr};
    float target_temperature{NAN};
    float current_temperature{NAN};
    climate::ClimateMode mode{climate::CLIMATE_MODE_OFF};
    climate::ClimateAction action{climate::CLIMATE_ACTION_OFF};
};

}  // namespace otgw
}  // namespace esphome
