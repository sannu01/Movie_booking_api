# Movie_booking_api

A movie ticket booking REST api using <b>python</b>,<b> Flask</b> and <b>MySql</b>.
The api provides booking ticket for a user providing Name,Phone Number and Ticket time.

It also checks for the available seats and only 20 tickets can be booked for a particular time.
However there is no restriction for the same person booking multiple tickets.
For booking a ticket it uses end point <b>"/book"</b> with the booking details in the json format and method should be <b>"POST"</b>.
![ticket_book](https://github.com/sannu01/Movie_booking_api/blob/master/output/ticket_book.png)

It provides an endpoint <b>"/view_ticket/timing"</b> to show all the tickets active for that particular time and it uses the method <b>"GET"</b>
and it return a list with all the tickets with their <b>ticketid</b> and <b>timing</b>.
![view_ticket](https://github.com/sannu01/Movie_booking_api/blob/master/output/view_ticket.png)

The endpoint <b>"/user/ticketid"</b> return the users details for that particular <b>ticketid</b>, it uses <b>"GET"</b> method.
![user_info](https://github.com/sannu01/Movie_booking_api/blob/master/output/user_info.png)
![user_info2](https://github.com/sannu01/Movie_booking_api/blob/master/output/user_info%20(2).png)

The endpoint <b>"/update_time"</b> takes json parameter having <b>ticketid</b> and <b>timing</b>, it checks for a valid futute time and then updates the time of the ticket.
It uses <b>"PUT"</b> method and return the updated details of the ticket.
![update_time](https://github.com/sannu01/Movie_booking_api/blob/master/output/update_ticket.png)
  
The endpoint <b>"/delete/ticketid"</b> deletes a ticket with requested <b>ticketid</b>, it checks for whether ticket id exist or not and then return the message on successful deletion. It uses <b>"DELETE"</b> method.
![delete](https://github.com/sannu01/Movie_booking_api/blob/master/output/delete_ticket.png)
 
 
The <b>api</b> automatically checks on some interval for expired ticket, if the difference between present time and ticket timing is more than <b>8 hours</b> the it <b>deletes</b> those tickets from database.


  
