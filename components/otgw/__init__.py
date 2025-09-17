import esphome.config_validation as cv
import esphome.codegen as cg

from esphome.components import uart, sensor

from esphome.const import CONF_ID

CODEOWNERS = ["@mvdnes"]
DEPENDENCIES = ["uart"]
AUTO_LOAD = ["sensor", "text_sensor"]

otgw_ns = cg.esphome_ns.namespace("otgw")
OpenThermGateway = otgw_ns.class_("OpenThermGateway", uart.UARTDevice, cg.Component)

CONF_OTGW_ID = "otgw_id"

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(OpenThermGateway),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(uart.UART_DEVICE_SCHEMA)
)

FINAL_VALIDATE_SCHEMA = uart.final_validate_device_schema(
    "otgw",
    baud_rate=9600,
    data_bits=8,
    parity="NONE",
    stop_bits=1,
    require_rx=True,
    require_tx=True,
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])

    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
