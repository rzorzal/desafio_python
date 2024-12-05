class FlightInsight(object):
    def __init__(self, data):
        self.airline = data['op_carrier']
        self.flight_number = data['op_carrier_fl_num']
        self.origin = data['origin']
        self.average_delay = data['avg_delay']
        self.total_air_time = data['total_air_time']
        self.amount_of_times_flew = data['flight_count']
        self.cancellation_chance = data['cancellation_chance']

    def to_dict(self):
        return dict({
            'airline': self.airline,
            'flight_number': self.flight_number,
            'origin': self.origin,
            'average_delay': self.average_delay,
            'total_air_time': self.total_air_time,
            'amount_of_times_flew': self.amount_of_times_flew,
            'cancellation_chance': self.cancellation_chance
        })