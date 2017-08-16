from units import ureg


@ureg.check(ureg.gpm, ureg.ft, ureg.rpm, None, None)
def calc_specific_speed(Q, H, n, double_entry=False, stages=1):
    """Calculate specific speed as per Lobanoff"""
    entries = 2 if double_entry else 1
    Ns = n * (Q / entries)**0.5 / (H / stages)**0.75
    return Ns.to(ureg.pump_Ns_us)
