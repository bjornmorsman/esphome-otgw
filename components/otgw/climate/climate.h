#pragma once

#include "esphome/core/component.h"
#include "esphome/components/climate/climate.h"
#include "esphome/components/otgw/otgw.h"
#include "esphome/components/sensor/sensor.h"

namespace esphome {
namespace otgw {

class OpenThermGatewayClimateThermostat : public climate::Climate, public Component {
public:
    void setup() override;
    void dump_config() override;
    climate::ClimateTraits traits() override;
    void control(const climate::ClimateCall& call) override;

    void set_parent(OpenThermGateway *parent) { this->parent_ = parent; }
    void set_target_temperature_constant(bool constant) { this->target_temperature_constant_ = constant; }
    void set_external_sensor(sensor::Sensor *sensor) { this->external_sensor_ = sensor; }

protected:
    OpenThermGateway *parent_{nullptr};
    bool target_temperature_constant_{false};
    sensor::Sensor *external_sensor_{nullptr};

    void on_otmessage(const OpenThermMessage &message);
    void on_timeout();
};

}  // namespace otgw
}  // namespace esphome
