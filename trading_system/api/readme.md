Endpoints
=========

All data has json format

/auth
-----

- `login`
    - in data:
        json with `username` and `password`
    - out data:
        json with `token`
        
- `logout`
    make token from query params invalid
    
- `register`
    - in data:
        json with `username`, `password`
    - out data:
        token
     
#####
TOKEN
#####
All endpoints below require user token
token provides like `www.example.com/path/to.endpoint?param1=value1&token=token&...`

/stocks
-------

- `/` (GET)
    return list of supported stocks
    
- `<tag>/history` (GET)
    return history for given stock 
    need to set range of dates for returning history
    `.../<tag>/history?from_date={from_date}&to_date={to_date}`
    date frormat '%d.%m.%Y'
    
    
/tickets
--------

- `/`
    - `GET` - return all user tickets
    - `POST` - create ticket for user
        MUST: 'stock_id', 'count', 'price', 'buy', 'duration'
        
- '/\<int:ticket_id\>'
    - `GET` - return ticket with given id if user is owner of it
    - `DELETE` - close ticket with given id if user is owner of it
    
- TODO: make user role brocker who can see tickets of his traders
