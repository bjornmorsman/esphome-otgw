import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate, sensor
from esphome.const import CONF_ID

from .. import otgw_ns, CONF_OTGW_ID, OpenThermGateway

DEPENDENCIES = ["otgw"]
CODEOWNERS = ["@mvdnes"]

OpenThermGatewayClimateThermostat = otgw_ns.class_(
    "OpenThermGatewayClimateThermostat", climate.Climate, cg.Component
)

CONF_TARGET_TEMPERATURE_CONSTANT = "target_temperature_constant"
CONF_EXTERNAL_TEMPERATURE_SENSOR = "external_temperature_sensor"

PLATFORM_SCHEMA = climate.CLIMATE_PLATFORM_SCHEMA.extend({
    cv.Optional(CONF_TARGET_TEMPERATURE_CONSTANT, default=False): cv.boolean,
    cv.Optional(CONF_EXTERNAL_TEMPERATURE_SENSOR): cv.use_id(sensor.Sensor),
})

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await climate.register_climate(var, config)

    if CONF_TARGET_TEMPERATURE_CONSTANT in config:
        cg.add(var.set_target_temperature_constant(config[CONF_TARGET_TEMPERATURE_CONSTANT]))

    if CONF_EXTERNAL_TEMPERATURE_SENSOR in config:
        ext_sensor = await cg.get_variable(config[CONF_EXTERNAL_TEMPERATURE_SENSOR])
        cg.add(var.set_external_sensor(ext_sensor))

# Dit is cruciaal: platform registreren zodat ESPHome 'id', 'name', etc. herkent
climate.register_climate_platform("otgw", PLATFORM_SCHEMA, to_code)
