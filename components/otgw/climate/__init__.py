import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate, sensor
from esphome.const import CONF_ID
from .. import otgw_ns, CONF_OTGW_ID, OpenThermGateway

OpenThermGatewayClimateThermostat = otgw_ns.class_(
    "OpenThermGatewayClimateThermostat", climate.Climate, cg.Component
)

SENSOR_ROOM_THERMOSTAT = "room_thermostat"
CONF_TARGET_TEMPERATURE_CONSTANT = "target_temperature_constant"
CONF_EXTERNAL_TEMPERATURE_SENSOR = "external_temperature_sensor"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_OTGW_ID): cv.use_id(OpenThermGateway),

    cv.Optional(SENSOR_ROOM_THERMOSTAT): climate.climate_schema(OpenThermGatewayClimateThermostat).extend({
        cv.GenerateID(): cv.declare_id(OpenThermGatewayClimateThermostat),
        cv.Optional(CONF_TARGET_TEMPERATURE_CONSTANT, default=False): cv.boolean,
        cv.Optional(CONF_EXTERNAL_TEMPERATURE_SENSOR): cv.use_id(sensor.Sensor),
    }),
})

async def to_code(config):
    parent = await cg.get_variable(config[CONF_OTGW_ID])

    if SENSOR_ROOM_THERMOSTAT in config:
        var = cg.new_Pvariable(config[SENSOR_ROOM_THERMOSTAT][CONF_ID])
        await cg.register_component(var, config[SENSOR_ROOM_THERMOSTAT])
        await climate.register_climate(var, config[SENSOR_ROOM_THERMOSTAT])
        cg.add(var.set_parent(parent))
        cg.add(var.set_target_temperature_constant(config[SENSOR_ROOM_THERMOSTAT][CONF_TARGET_TEMPERATURE_CONSTANT]))

        if CONF_EXTERNAL_TEMPERATURE_SENSOR in config[SENSOR_ROOM_THERMOSTAT]:
            ext_sensor = await cg.get_variable(config[SENSOR_ROOM_THERMOSTAT][CONF_EXTERNAL_TEMPERATURE_SENSOR])
            cg.add(var.set_external_sensor(ext_sensor))
