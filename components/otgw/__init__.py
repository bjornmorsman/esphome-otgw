import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.components import uart, sensor, climate
from esphome.const import CONF_ID

CODEOWNERS = ["@mvdnes"]
DEPENDENCIES = ["uart"]
AUTO_LOAD = ["sensor", "text_sensor", "climate"]  # include submodules

# Namespace
otgw_ns = cg.esphome_ns.namespace("otgw")
OpenThermGateway = otgw_ns.class_("OpenThermGateway", uart.UARTDevice, cg.Component)

CONF_OTGW_ID = "otgw_id"

# Room thermostat constants
SENSOR_ROOM_THERMOSTAT = "room_thermostat"
CONF_TARGET_TEMPERATURE_CONSTANT = "target_temperature_constant"
CONF_EXTERNAL_TEMPERATURE_SENSOR = "external_temperature_sensor"

# CONFIG_SCHEMA inclusief externe sensor
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(OpenThermGateway),
    cv.Optional(SENSOR_ROOM_THERMOSTAT): cv.Schema({
        cv.GenerateID(): cv.declare_id(climate.OpenThermGatewayClimateThermostat),
        cv.Optional(CONF_TARGET_TEMPERATURE_CONSTANT, default=False): cv.boolean,
        cv.Optional(CONF_EXTERNAL_TEMPERATURE_SENSOR): cv.use_id(sensor.Sensor),
    }).extend(climate.CLIMATE_SCHEMA),
}).extend(cv.COMPONENT_SCHEMA).extend(uart.UART_DEVICE_SCHEMA)

# UART default validatie
FINAL_VALIDATE_SCHEMA = uart.final_validate_device_schema(
    "otgw",
    baud_rate=9600,
    data_bits=8,
    parity="NONE",
    stop_bits=1,
    require_rx=True,
    require_tx=True,
)

# Import submodules
from . import climate

# Codegen
async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if SENSOR_ROOM_THERMOSTAT in config:
        conf = config[SENSOR_ROOM_THERMOSTAT]
        var_climate = cg.new_Pvariable(conf[CONF_ID])
        await cg.register_component(var_climate, conf)
        await climate.register_climate(var_climate, conf)

        # Koppel parent en target temperature constant
        cg.add(var_climate.set_parent(var))
        cg.add(var_climate.set_target_temperature_constant(
            conf.get(CONF_TARGET_TEMPERATURE_CONSTANT, False)
        ))

        # Koppel externe sensor indien aanwezig
        if CONF_EXTERNAL_TEMPERATURE_SENSOR in conf:
            ext_sensor = await cg.get_variable(conf[CONF_EXTERNAL_TEMPERATURE_SENSOR])
            cg.add(var_climate.set_external_sensor(ext_sensor))
