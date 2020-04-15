const es = new ReconnectingEventSource('/events/')

//notifications panel
es.addEventListener('messages', (event)=>{
    const event_data =  JSON.parse(event.data)
    console.log(event_data)
})