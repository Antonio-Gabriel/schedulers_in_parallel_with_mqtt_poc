#  Schedulers in parallel with mqtt poc

The service needs to run parallel to the server, observing all registered dates and sending a notification to the mqtt broker when a scheduled time matches, sending data and notifying a front end via socket. 

## Features

- [x] Release an endpoint to record and list a date and its times
- [x] Create threads to register 2 threads to run each timetable observation process
- [x] Create a local database service where the timetables will be stored
- [ ] Add validation to check if certain schedules have already been triggered on a given day, if so ignore them and take others.
- [ ] Create a service to send encoded audio and some data to mqtt
- [ ] Create a real-time communication channel via radio frequency
- [x] Get the api and cron services running in parallel
