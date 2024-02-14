-- Keep a log of any SQL queries you execute as you solve the mystery.

-- 1. crime scene  report
SELECT id, description FROM crime_scene_reports
WHERE day = 28
    AND month = 7
    AND year = 2021
    AND street LIKE 'Humphrey Street';

--2. interviews
SELECT id, name, transcript FROM interviews
WHERE year = 2021
    AND month = 7
    AND day = 28
    AND transcript LIKE '%bakery%';

--3. details of person who leaves the bakery's parking lot
SELECT  p.id, name, phone_number, passport_number, p.license_plate
FROM people p, bakery_security_logs b
WHERE day = 28
    AND year = 2021
    AND month = 7
    AND hour = 10
    AND minute BETWEEN 15 AND 25
    AND activity like "exit"
    AND p.license_plate = b.license_plate;

--4.person details who did transaction, and leaves from bakery's parking lot.
SELECT  bk.person_id , bk.creation_year, p.name , p.phone_number, p.passport_number, p.license_plate
FROM people p, bakery_security_logs b,  bank_accounts bk, atm_transactions t
WHERE b.day = 28
    AND b.year = 2021
    AND b.month = 7
    AND b.hour = 10
    AND b.minute BETWEEN 15 AND 25
    AND b.activity like "exit"
    AND p.license_plate = b.license_plate
    AND t.account_number = bk.account_number
    and p.id = bk.person_id
    AND t.atm_location like 'Leggett Street'
    AND t.transaction_type LIKE 'withdraw';

--5. theif made phone call less than minute to arrage fligth tickets.
SELECT id, caller, receiver, duration FROM phone_calls
WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration < 60;

--6. Earliest fligths that take off from the fiftyville airport on 29 July.
SELECT f.id, a.abbreviation,a.full_name, a.city, f.origin_airport_id , f.destination_airport_id, f.hour, f.minute
FROM flights f, airports a
where f.year = 2021
and f.day = 29
AND f.month = 7
AND a.city LIKE 'Fiftyville'
AND a.id = f.origin_airport_id
ORDER BY f.hour,f.minute
LIMIT 1;

--7 Passsangers in earliest flight which takes off from fiftyville airport on 29 july.
SELECT * FROM passengers pass , people p
WHERE p.passport_number = pass.passport_number
AND pass.flight_id IN
(SELECT f.id
FROM flights f, airports a
where f.year = 2021
and f.day = 29
AND f.month = 7
AND a.city LIKE 'Fiftyville'
AND a.id = f.origin_airport_id
ORDER BY f.hour,f.minute
LIMIT 1)
AND p.phone_number in
(SELECT caller FROM phone_calls
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration < 60);

 --8 Passangers in the earliest flight, Which takes off from fiftyville airport on 29 july,
 -- and who made call less than one min and who leaves from bakery's parking lot and also made transaction on Leggret street
SELECT  bk.person_id , bk.creation_year, p.name , p.phone_number, p.passport_number, p.license_plate
FROM people p, bakery_security_logs b,  bank_accounts bk, atm_transactions t
WHERE b.day = 28
    AND b.year = 2021
    AND b.month = 7
    AND b.hour = 10
    AND b.minute BETWEEN 15 AND 25
    AND b.activity like "exit"
    AND p.license_plate = b.license_plate
    AND t.account_number = bk.account_number
    and p.id = bk.person_id
    AND t.atm_location like 'Leggett Street'
    AND t.transaction_type LIKE 'withdraw'
    AND p.license_plate IN
-- person who leaves from bakrey's parking lot within time frame
    (SELECT p.license_plate FROM passengers pass , people p
    WHERE p.passport_number = pass.passport_number
    AND pass.flight_id IN
-- Earliest flight that take off from fiftyville airport onn 29 JULY 2021
    (SELECT f.id
    FROM flights f, airports a
    where f.year = 2021
    and f.day = 29
    AND f.month = 7
    AND a.city LIKE 'Fiftyville'
    AND a.id = f.origin_airport_id
    ORDER BY f.hour,f.minute
    LIMIT 1)
    AND p.phone_number IN
-- call less than one minute
    (SELECT caller FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 60));

-- Name of Accomplisher of thief
SELECT name FROM people WHERE
phone_number in(
SELECT receiver FROM phone_calls
   WHERE duration < 60
   AND year = 2021
   AND year = 2021
   AND month = 7
   AND day = 28
   AND caller LIKE '(367) 555-5533');

-- Name of the city where the thief and its accomplisher escaped.
SELECT city FROM airports
WHERE id IN(
    SELECT f.destination_airport_id
    FROM flights f, airports a
    where f.year = 2021
    and f.day = 29
    AND f.month = 7
    AND a.city LIKE 'Fiftyville'
    AND a.id = f.origin_airport_id
    ORDER BY f.hour,f.minute
    LIMIT 1);