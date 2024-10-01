import pandas as pd
from django.core.management.base import BaseCommand
from products.models import WPCustomer
from datetime import datetime

class Command(BaseCommand):
    help = 'Import customers from old_customers.csv into the WPCustomer model'

    def handle(self, *args, **kwargs):
        # Load the CSV file
        file_path = 'wp_customers.csv'
        try:
            df = pd.read_csv(file_path)

            for index, row in df.iterrows():
                # Clean up and extract data from each row
                user_id = row['User ID']
                username = row['Username']
                phone = '0' + username[2:]
                user_role = row.get('User Role', 'customer')  # Default to 'customer' if not provided
                first_name = row['First Name']
                last_name = row['Last Name']
                full_name = row['Full Name']
                nickname = row.get('Nickname', None)
                email = row.get('E-mail', None)
                orders = row.get('Orders', None)
                money_spent = row.get('Money Spent', None)
                website = row.get('Website', None)
                date_registered = row.get('Date Registered')
                biographical_info = row.get('Biographical Info', None)

                # Convert date_registered to a datetime object
                if isinstance(date_registered, str):
                    try:
                        date_registered = datetime.strptime(date_registered, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        self.stdout.write(f"Skipping row with invalid date: {row}")
                        continue

                # Save the customer in the database
                try:
                    WPCustomer.objects.update_or_create(
                        user_id=user_id,
                        defaults={
                            'username': username,
                            'phone': phone,
                            'user_role': user_role,
                            'first_name': first_name,
                            'last_name': last_name,
                            'full_name': full_name,
                            'nickname': nickname,
                            'email': email,
                            'orders': orders if pd.notna(orders) else None,
                            'money_spent': money_spent if pd.notna(money_spent) else None,
                            'website': website,
                            'date_registered': date_registered,
                            'biographical_info': biographical_info
                        }
                    )
                    self.stdout.write(self.style.SUCCESS(f"Successfully added/updated user {username}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to save user {username}: {e}"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found"))
