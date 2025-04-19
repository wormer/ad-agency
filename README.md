# Ad Agency Budget Management — Test Assignment

This project simulates an Ad Agency that manages multiple brands, each with its own daily and monthly budget.

### Key rules:

- If a brand exceeds its **daily budget**, all campaigns are paused for the rest of the day.
- If a brand exceeds its **monthly budget**, all campaigns are paused for the rest of the month.
- At the start of a **new day/month**, campaigns are re-evaluated and can be turned back on if budgets allow.
- Some campaigns follow **dayparting**: they run only during specific hours of the day.

---

## How to Run

### Clone and run the project

```bash
git clone https://github.com/wormer/ad-agency.git
cd ad-agency
pip install -r requirements.txt
src/manage.py migrate
src/manage.py runserver
```

### Run tests

```bash
src/manage.py test aa
```

---

## Data Structures

### Brand

- `id`: integer
- `name`: string
- `monthly_budget`: decimal
- `daily_budget`: decimal
- `dayparting`: list of time ranges `[["HH:MM", "HH:MM"], ...]`

### Spend

- `id`: integer
- `brand_id`: foreign key to Brand
- `datetime`: timestamp of the spend
- `amount`: decimal

---

## Flow of the Program

### Brand Management

- Create new brands
- List all brands
- Update brand name, budgets, and dayparting schedule

### Spend Management

- Register new spends for a brand
- Check daily/monthly spending
- Retrieve campaign status (active/inactive)

### Internal Logic

- Campaign status is determined dynamically when queried.
- Campaigns become active again automatically if budget allows and day/month has reset.
- Dayparting is respected during status checks.
- Spend registration always succeeds regardless of campaign status.

## Assumptions and Simplifications

- **No DRF or serializers used** – the project uses plain Django views and models, without Django REST Framework or input validation.
- **No authentication or authorization** – all endpoints are open and unauthenticated.
- **Campaigns are toggled globally per brand** – there is no concept of individual campaigns; the brand as a whole is either active or inactive.
- **Campaign status is not cached** – it's recalculated every time it is queried based on current time and spends.
- **Spends can be registered regardless of campaign status** – the system does not prevent spending when a campaign is inactive. It is the client's responsibility to check the status before spending. Once a spend is registered, it is final.
- **Server-local time is used** – there is no timezone handling or normalization.
- **No error handling** – the focus is on demonstrating business logic, not on handling edge cases or invalid inputs.

---

## API Endpoints

### 🔹 List Brands

`GET /brand/`  
Returns a list of all brands.

```json
{
  "brands": [
    {
      "id": 1,
      "name": "Client"
    },
    {
      "id": 2,
      "name": "Company"
    }
  ]
}
```

---

### 🔹 Create Brand

`POST /brand/`

**Request:**

```json
{
  "name": "Company",
  "daily_budget": 10,
  "monthly_budget": 1000,
  "dayparting": [
    ["10:00", "12:00"],
    ["15:00", "17:00"]
  ]
}
```

**Response:**

```json
{ "id": 4 }
```

---

### 🔹 Get Brand Details

`GET /brand/1/`

```json
{
  "name": "Company",
  "monthly_budget": "1000.00",
  "daily_budget": "10.00",
  "dayparting": [
    ["10:00", "12:00"],
    ["15:00", "17:00"]
  ]
}
```

---

### 🔹 Update Brand

`POST /brand/1/`

**Request:**

```json
{
  "monthly_budget": 5000,
  "dayparting": [
    ["10:05", "12:05"],
    ["15:05", "17:05"]
  ]
}
```

**Response:**

```json
{}
```

---

### 🔹 Campaign Status

`GET /brand/1/status/`

```json
{
  "spends_this_month": "40.70",
  "spends_today": "0.00",
  "is_active": false
}
```

---

### 🔹 Register Spend

`POST /spend/1/`

**Request:**

```json
{
  "amount": 0.7
}
```

**Response:**

```json
{}
```

## Pseudocode

### 1. **`brand_list`** - View for getting a list of brands or creating a new brand.

```pseudo
function brand_list(request):
    if request method is GET:
        return a list of all brands with their id and name
    if request method is POST:
        parse data from the request (name, monthly_budget, daily_budget, dayparting)
        create a new brand with the provided data
        return the id of the newly created brand
```

### 2. **`brand_details`** - View for getting and updating the details of a specific brand.

```pseudo
function brand_details(request, brand_id):
    find the brand by its id
    if request method is POST:
        update the brand's name, monthly_budget, daily_budget, or dayparting based on the request data
        save the updated brand information
    return the brand's details as JSON (name, monthly_budget, daily_budget, dayparting)
```

### 3. **`register_spend`** - View for registering a spend for a specific brand.

```pseudo
function register_spend(request, brand_id):
    find the brand by its id
    if request method is POST:
        parse amount from the request data
        create a new Spend record for the brand with the given amount
    return a success response
```

### 4. **`campaign_status`** - View for checking the current campaign status for a specific brand.

```pseudo
function campaign_status(request, brand_id):
    find the brand by its id
    get the current time
    calculate total spends for today and this month
    check if the current time respects the brand's dayparting schedule
    determine if the campaign is active based on the budget and dayparting
    return the campaign status (spends today, spends this month, and if the campaign is active)
```
