# OpenTherm Gateway integration for ESPHome

This plugin intends to parse the serial communication as provided by an OpenTherm Gateway (OTGW). The OTGW project can be found here: https://otgw.tclcode.com/

The main entity is the climate integration which allows viewing and controlling of the room setpoint.

For other sensors, only a subset of OTGW messages are parsed. New sensors can be added fairly easily by modifying `otgw/sensor/__init__.py`. Feel free to make a pull-request.

## Example Configuration

```yaml
external_components:
  - source: github://bjornmorsman/esphome-otgw

uart:
  # Serial for OTGW PIC
  - id: uart_otgw
    baud_rate: 9600
    tx_pin: GPIO1
    rx_pin: GPIO3
    data_bits: 8
    parity: NONE
    stop_bits: 1

otgw:
  uart_id: uart_otgw

climate:
  - platform: otgw
    room_thermostat:
      name: Thermostat

sensor:
  - platform: otgw
    control_setpoint:
      name: Control Setpoint
    room_setpoint:
      name: Room Setpoint
    central_heating_water_pressure:
      name: Central Heating Water Pressure
    room_temperature:
      name: Room Temperature
    boiler_water_temperature:
      name: Boiler Water Temperature
    burner_operation_hours:
      name: Burner Operation Hours
    burner_starts:
      name: Burner Starts
    max_relative_modulation_level:
      name: Max Relative Modulation Level
    relative_modulation_level:
      name: Relative Modulation Level

binary_sensor:
  - platform: otgw
    fault_indication:
      name: Fault Indication
    ch_active:
      name: Central Heating State
    dhw_active:
      name: Domestic Hot Water State
    flame_status:
      name: Flame Status

text_sensor:
  - platform: otgw
    version:
      name: OTGW version
```

Optional additional configuration to ensure a reset of the OTGW PIC when ESPHome is reloaded:

```yaml
esphome:
  # ...other config options...
  on_boot:
    # Reset the OTGW PIC
    # This ensures the debug output of the esp on the serial output does not confuse the PIC
    priority: 600
    then:
      - output.turn_off: pic_reset_n
      - delay: 100ms
      - output.turn_on: pic_reset_n

output:
  # Reset line of the OTGW PIC
  - platform: gpio
    pin:
      number: GPIO14
      mode:
        output: true
        open_drain: true
    id: pic_reset_n
```

