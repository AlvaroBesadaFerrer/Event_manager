def list_to_string(lista):
    # Cambiamos las listas por strings porque los st.dataframe y st.table no soportan listas y da un warning en la consola
    output = ""
    for elem in lista:
        output+= elem.name + " "

    return output.strip()


def show_details(event):

    return {
        "spot": event.spot.name,
        "event_type": event.event_type.name,
        "workers": list_to_string(event.workers),
        "resources": list_to_string(event.resources),
        "start_date": event.date.strftime('%Y-%m-%d'),
        "start_time": event.start_time.strftime('%H:%M:%S'),
        "end_time": event.end_time.strftime('%H:%M:%S'),
    }