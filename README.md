

# GigVerse: A Microjobs and Gigs Platform

![logo](https://i.ibb.co/KF0RmZG/logo.png)


GigVerse is a web application designed as a platform for microjobs and gig listings, where users can post simple tasks (gigs) and interact through job approvals, deposits, withdrawals, and payments. The platform acts as a secure intermediary between gig sellers (workers) and buyers, ensuring transparency and reliability during the transaction process. This project was developed using Django, JavaScript, HTML, and CSS.

## Distinctiveness and Complexity

### Distinctiveness
GigVerse stands out from the standard Django projects due to its specific focus on handling microtransactions between users, managing user wallets, and updating proof statuses through asynchronous JavaScript actions. Unlike a simple blog or e-commerce site, GigVerse incorporates dynamic features such as wallet management, job approval systems, and real-time balance updates, which require more intricate database handling and frontend-backend communication.

This project is unique because it simulates a real-world platform for microjobs, where interactions between users are mediated by the system. The wallet, deposit, and withdrawal functionalities are designed to enhance the user's experience by handling digital transactions within the platform.
### Complexity
The complexity lies in several aspects of the project:

- **Wallet Management:** The system allows users to deposit and withdraw virtual currency, with real-time balance updates stored in the database.
- **Proof Status Updates:** Admins or job owners can approve or decline proofs submitted by workers. Approvals and declines trigger specific actions, such as adding money to the worker's wallet or refunding the job owner.
- **Dynamic Frontend Integration:** The platform uses JavaScript to handle asynchronous requests for proof status changes, enabling real-time updates without reloading the page.
- **Database Relationships:** The project manages complex relationships between models such as `User`, `Wallet`, `Job`, and `Proof`. It also ensures that constraints such as job ownership and wallet balance are respected.

These features require a solid understanding of Django, database modeling, and frontend-backend integration, making the project both distinctive and complex.

## What's Contained in Each File

- **`jobs/models.py`**: Contains the Django models for `User`, `Job`, `Proof`, and `Wallet`. These models represent the core entities of the platform, including relationships between users, jobs, and their respective wallets.
  
- **`jobs/views.py`**: Defines the logic for wallet management, job handling, and proof status updates. It includes the `deposit`, `withdrawal`, `wallet`, and `change_stat` views for handling the main interactions in the app.

- **`jobs/templates/jobs/`**: Contains HTML templates for rendering pages such as the wallet page, job listings, and profile views. Templates are modular, with `layout.html` serving as the base layout.

- **`jobs/static/jobs/`**: Contains static files such as JavaScript and CSS. The `wallet.js` file is used to manage asynchronous operations on proof status updates.

- **`jobs/urls.py`**: Maps URLs to views, defining routes for handling requests like changing proof status, viewing wallets, and managing jobs.

- **`wallet.js`**: Handles the client-side logic for updating the proof status using JavaScript and Fetch API to send asynchronous requests to the server without page reload.
  
## How to Run the Application

1. **Install Project Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Apply Database Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```


3. **Start the Development Server**

   ```bash
   python manage.py runserver
   ```

4. **Access the site**:
   Open your web browser and go to `http://127.0.0.1:8000/` to access the platform.

## Additional Information

- **Job Posting and Proof Approval Workflow**:
   - **Buyers**: Post jobs on the platform with a description of the required task and payment.
   - **Workers**: Complete jobs and submit proof of completion (such as screenshots or URLs).
   - **Buyers**: Review and approve or decline the proof.
   - If approved, the payment is transferred from the buyer’s wallet to the worker's wallet. If declined, the payment is refunded to the buyer's wallet.
   
- **Wallet System**:
   - Users can deposit funds into their wallets to use for posting jobs and paying workers.
   - Workers receive payments in their wallets once a job is approved and can withdraw funds when they accumulate a balance.

- **Asynchronous Proof Updates**:
   - The `wallet.js` file handles proof approval and declines through asynchronous requests, allowing the user to interact with the system without page reloads.

---







