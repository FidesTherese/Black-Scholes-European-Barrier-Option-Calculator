from .BarrierOptionCalculator import BarrierOption

# For in-barrier
IN_BARRIER_OPTIONS = {
    'up-and-in-call',
    'up-and-in-put',
    'down-and-in-call',
    'down-and-in-put',
}

# Detect if the in-barrier option is knocked in
def price(option_type: str, *, knocked_in: bool = None, **kwargs) -> float:
    if option_type in IN_BARRIER_OPTIONS and knocked_in is None:
        raise ValueError(
            f"[ERROR] Option type '{option_type}' requires you to explicitly specify whether it has knocked in or not using knocked_in=True or False."
        )
    option = BarrierOption(**kwargs)
    # Route
    if option_type == 'up-and-out-call':
        return option.up_and_out_call()
    elif option_type == 'up-and-in-call':
        return option.up_and_in_call(knocked_in = knocked_in)
    elif option_type == 'down-and-out-call':
        return option.down_and_out_call()
    elif option_type == 'down-and-in-call':
        return option.down_and_in_call(knocked_in = knocked_in)
    elif option_type == 'down-and-out-put':
        return option.down_and_out_put()
    elif option_type == 'down-and-in-put':
        return option.down_and_in_put(knocked_in = knocked_in)
    elif option_type == 'up-and-out-put':
        return option.up_and_out_put()
    elif option_type == 'up-and-in-put':
        return option.up_and_in_put(knocked_in = knocked_in)
    else:
        raise NotImplementedError(f"Option type '{option_type}' is not supported.")