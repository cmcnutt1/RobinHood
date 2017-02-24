def create_port_list(port_of_call_list):
    port_list = ""

    for port in port_of_call_list:
        port_list = port_list + port + "<br>"

    port_list = port_list[0:len(port_list)-4]

    return port_list

def test_HTML_input(departure_location, arrival_location, port_list, standard_price):
    html_port_list = create_port_list(port_list)
    HTML_input = """<table class ="table table-bordered tours-tabs__table" style="height: 233px; width: 844px;">
    <tbody>

    <tr>
    <td style = "width: 296px;"><strong>PORT OF DEPARTURE</strong></td>
    <td style = "width: 550px;">""" + departure_location + """</td>
    </tr>

    <tr>
    <td style = "width: 296px;"><strong>PORTS OF CALL</strong></td>
    <td style = "width: 550px;" >""" + html_port_list + """</td>
    </tr>

    <tr>
    <td style = "width: 296px;"><strong>PORT OF ARRIVAL</strong></td>
    <td style = "width: 550px;">""" + arrival_location + """</td>
    </tr>

    <tr>
    <td style = "width: 296px;"><strong>INCLUDED</strong></td>
    <td style = "width: 550px;">
    <table class ="table table-bordered" style="height: 62px;" width="300">
    <tbody>
    <tr>
    <td>[icon_tick state = "on"]Accommodations</td>
    <td>[icon_tick state = "on"]On-board Entertainment</td>
    </tr>
    <tr>
    <td>[icon_tick state = "on"]Dining</td>
    <td>[icon_tick state = "on"]Taxes, Fees, Port Expenses</td>
    </tr>
    </tbody>
    </table>
    </td>
    </tr>

    <tr>
    <td style = "width: 296px;"><strong>NOT INCLUDED</strong></td>
    <td style = "width: 550px;">
    <table class ="table table-bordered" style="height: 62px;" width="300">
    <tbody>
    <tr>
    <td> [icon_tick state = "off"]Gratuities</td>
    <td> [icon_tick state = "off"]Premium Dining</td>
    </tr>
    <tr>
    <td> [icon_tick state = "off"]Shore Excursion Costs</td>
    <td> [icon_tick state = "off"]Holiday Events and Celebrations</td>
    </tr>
    </tbody>
    </table>
    </td>
    </tr>

    <tr>
    <td style = "width: 296px;"><strong>CABIN TYPES</strong></td>
    <td style = "width: 550px;">
    <table class ="table table-bordered" style="height: 62px;" width="300">
    <tbody>
    <tr>
    <td>[icon_tick state = "on"]Interior</td>
    <td>[icon_tick state = "on"]Outside View</td>
    </tr>
    <tr>
    <td>[icon_tick state = "on"]Balcony</td>
    <td>[icon_tick state = "on"]Suite</td>
    </tr>
    </tbody>
    </table>
    <span style = "font-size: 8pt;">
    <strong>Note:</strong>Prices start at <strong>$""" + standard_price + """ </strong>but vary by cabin type and are always changing. Consult an Interline Advantage representative using the booking form for the most up-to-date pricing.</span></td>
    </tr>
    </tbody>
    </table>"""

    #change to return?
    return HTML_input

if __name__ == '__main__':
    departure_location = "Testing Departure, NJ"
    arrival_location = "Testing Arrival, FL"
    port_of_call_list = ["Test Port 1", "Test Port 2", "Test Port 3"]
    standard_price = "1000"
    port_list = create_port_list(port_of_call_list)
    test_HTML_input(departure_location, port_list, standard_price)
