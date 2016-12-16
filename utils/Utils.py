

V_dd = 5  # Positive supply voltage
V_ss = 0  # Ground

V_ref = V_dd  # MCP3201 reference voltage
D_max = 4096  # MCP3201 max digital output

R_div = 100  # Voltage divider resistance

A = 3379.55
B = 0.000142687
C = 646108135948007
D = 851248760000


def digital_to_voltage(d_in):
    """
    Calculate the input voltage for a input value.
    Dout = (4096 * Vin) / Vref
    :param d_in: digital input value
    :return: digital input converted to input voltage
    """
    return (V_ref * d_in) / D_max


def voltage_to_resistance(v_in):
    """
    Calculate the PT100 resistance value for a given measured voltage over the PT100, given the resistance for
    the voltage divider.
    R_pt100 = (Vin * Rdiv) / (Vdd - Vin)
    :param v_in: input voltage
    :return: r_out(v_in)
    """
    return (v_in * R_div) / (V_dd - v_in)


def resistance_to_temperature(r_in):
    """
    Calculate the temperature from the measured resistance of the PT100.
    :param r_in: input resistance
    :return: temperature(r_in)
    """
    return A - B * (C - D * r_in) ** 0.5


def digital_to_temp(d_in):
    """
    Calculate the measured input temperature from the sampled input value.
    :param d_in: digital input value
    :return: temperature(d_in)
    """
    v_in = digital_to_voltage(d_in)
    r_in = voltage_to_resistance(v_in)
    t_in = resistance_to_temperature(r_in)
    return t_in
