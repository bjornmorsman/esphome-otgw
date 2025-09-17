import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate, sensor
from esphome.const import CONF_ID
from .. import otgw_ns, CONF_OTGW_ID, OpenThermGateway

DEPENDENCIES = ["otgw"]
CODEOWNERS = ["@mvdnes"]

# C++ klasse
OpenThermGatewayClimateThermostat = otgw_ns.class_(
    "OpenThermGatewayClimateThermostat", climate.Climate, cg.Component
)

# Config keys
SENSOR_ROOM_THERMOSTAT = "room_thermostat"
CONF_TARGET_TEMPERATURE_CONSTANT = "target_temperature_constant"
CONF_ROOM_TEMPERATURE_SOURCE = "room_temperature_source"
CONF_EXTERNAL_ROOM_SENSOR = "external_room_sensor"

# Schema
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_OTGW_ID): cv.use_id(OpenThermGateway),

    cv.Optional(SENSOR_ROOM_THERMOSTAT): climate.climate_schema(OpenThermGatewayClimateThermostat).extend({
        cv.GenerateID(): cv.declare_id(OpenThermGatewayClimateThermostat),
        cv.Optional(CONF_TARGET_TEMPERATURE_CONSTANT, default=False): cv.boolean,
        cv.Optional(CONF_ROOM_TEMPERATURE_SOURCE, default="otgw"): cv.enum({
            "otgw": otgw_ns.RoomTemperatureSource.OTGW_THERMOSTAT,
            "external": otgw_ns.RoomTemperatureSource.EXTERNAL_SENSOR,
        }),
        cv.Optional(CONF_EXTERNAL_ROOM_SENSOR): cv.use_id(sensor.Sensor),
    }),
})

# Binding YAML naar C++
async def to_code(config):
    parent = await cg.get_variable(config[CONF_OTGW_ID])

    if SENSOR_ROOM_THERMOSTAT in config:
        var = cg.new_Pvariable(config[SENSOR_ROOM_THERMOSTAT][CONF_ID])
        await cg.register_component(var, config[SENSOR_ROOM_THERMOSTAT])
        await climate.register_climate(var, config[SENSOR_ROOM_THERMOSTAT])

        # Parent OTGW instellen
        cg.add(var.set_parent(parent))

        # Target temperature constant
        cg.add(var.set_target_temperature_constant(
            config[SENSOR_ROOM_THERMOSTAT][CONF_TARGET_TEMPERATURE_CONSTANT]
        ))

        # Room temperature source (OTGW of external)
        cg.add(var.set_room_temperature_source(
            config[SENSOR_ROOM_THERMOSTAT][CONF_ROOM_TEMPERATURE_SOURCE]
        ))

        # Externe sensor
        if CONF_EXTERNAL_ROOM_SENSOR in config[SENSOR_ROOM_THERMOSTAT]:
            cg.add(var.set_external_room_sensor(
                config[SENSOR_ROOM_THERMOSTAT][CONF_EXTERNAL_ROOM_SENSOR]
            ))
