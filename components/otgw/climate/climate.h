#pragma once

#include "esphome/core/component.h"
#include "esphome/components/climate/climate.h"
#include "esphome/components/sensor/sensor.h"  // nodig voor externe sensor
#include "esphome/components/otgw/otgw.h"

namespace esphome {
namespace otgw {

// Keuze van bron voor kamertemperatuur
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
  void loop() override;  // voor externe sensor

  void set_parent(OpenThermGateway *parent) { this->parent_ = parent; }
  void set_target_temperature_constant(bool constant) { this->target_temperature_constant_ = constant; }

  void set_room_temperature_source(RoomTemperatureSource src) { this->room_temp_source_ = src; }
  void set_external_room_sensor(sensor::Sensor *sensor) { this->external_room_sensor_ = sensor; }

 protected:
  OpenThermGateway *parent_;
  bool target_temperature_constant_{false};

  RoomTemperatureSource room_temp_source_{RoomTemperatureSource::OTGW_THERMOSTAT};
  sensor::Sensor *external_room_sensor_{nullptr};

  void on_otmessage(const OpenThermMessage &message);
  void on_timeout();
};
}  // namespace otgw
}  // namespace esphome
