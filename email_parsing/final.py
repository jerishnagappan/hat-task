import tkinter as tk
from tkinter import messagebox, scrolledtext
import imaplib
import email
from email.policy import default
import psycopg2
import re
import requests
import json
import os

class EmailApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gmail Viewer")
        self.master.geometry("800x800")

        self.email_frame = tk.Frame(master, width=300)
        self.email_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.email_vars = []
        self.email_listbox = tk.Frame(self.email_frame)
        self.email_listbox.pack(pady=20)

        self.load_emails_button = tk.Button(self.email_frame, text="Load Emails", command=self.load_emails, bg="black", fg="black")
        self.load_emails_button.pack(pady=10)

        self.save_emails_button = tk.Button(self.email_frame, text="Save Selected Emails", command=self.save_selected_emails, bg="blue", fg="black")
        self.save_emails_button.pack(pady=10)

        self.content_frame = tk.Frame(master)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.email_preview = scrolledtext.ScrolledText(self.content_frame, wrap=tk.WORD, height=30)
        self.email_preview.pack(pady=20, fill=tk.BOTH, expand=True)

    def load_emails(self):
        self.emails = self.fetch_emails()
        for widget in self.email_listbox.winfo_children():
            widget.destroy()  

        self.email_vars.clear() 

        if not self.emails:
            messagebox.showinfo("Info", "No emails found.")
        else:
            for email_info in self.emails:
                var = tk.IntVar()  
                checkbox = tk.Checkbutton(self.email_listbox, text=f"{email_info['from']} - {email_info['subject']}", variable=var)
                checkbox.pack(anchor='w')  
                self.email_vars.append((var, email_info))  

    def fetch_emails(self):
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login('testinghashagile@gmail.com', 'oyzp lusb dbsm bpmp')  
            mail.select('inbox')

            result, data = mail.search(None, 'ALL')
            if result == 'OK':
                email_ids = data[0].split()
                email_data = []

                for e_id in email_ids:
                    result, msg_data = mail.fetch(e_id, '(RFC822)')
                    if result != 'OK':
                        raise Exception("Failed to fetch email data.")

                    msg = email.message_from_bytes(msg_data[0][1], policy=default)
                    body, attachments = self.get_email_body(msg)
                    email_data.append({
                        'subject': msg['subject'],
                        'from': msg['from'],
                        'date': msg['date'],
                        'body': body,
                        'attachments': attachments  
                    })
                mail.logout()
                return email_data
            else:
                raise Exception("Failed to retrieve email IDs.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch emails: {e}")
            return []  

    def get_email_body(self, msg):
        body = ""
        attachment_filenames = []

        if msg.is_multipart():
            for part in msg.iter_parts():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode(part.get_content_charset(), errors='ignore')
                elif part.get_content_disposition() == 'attachment':
                    filename = part.get_filename()
                    if filename:
                        
                        with open(filename, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        attachment_filenames.append(filename)
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset(), errors='ignore')

        return body, attachment_filenames

    def save_selected_emails(self):
        for var, email_info in self.email_vars:
            if var.get() == 1:  
                self.store_email_in_db(email_info)

    def store_email_in_db(self, email_info):
        subject = email_info['subject']
        sender = email_info['from']
        date = email_info['date']  
        body = email_info['body']
        attachments = ', '.join(email_info['attachments'])  
        
        
        candidate_name = self.extract_name_from_email(sender)
        entry_time = date  
        try:
            conn = psycopg2.connect(
                dbname='mydb',     
                user='jerish_nagappan',   
                password='1234', 
                host='localhost',
                port='5433'
            )
            cur = conn.cursor()

            cur.execute("""
            INSERT INTO email_enter (subject, sender, date, body, attachment_filename, candidate_name, entry_time)
            VALUES (%s, %s, %s::date, %s, %s, %s, %s::date);
            """, (subject, sender, date, body, attachments, candidate_name, entry_time))

            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("Success", f"Email '{subject}' stored successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to store email data: {e}")

    def parse_email_content(self, email_body):
        try:
            url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
            headers = {
                'Content-Type': 'application/json',
            }
            payload = {
                'contents': [{
                    'parts': [{
                        'text': f"Extract key points like name, email, contact_number, education (degree, major, university, year_of_passout), college_name, skills, internship_experiences, soft_skills, languages-known from the following content:\n{email_body}"
                    }]
                }]
            }

            response = requests.post(url, headers=headers, json=payload, params={'key': 'AIzaSyAZObkM-GACE7hs1Z7m5fnwPjVFQ6zmOqw'})

            if response.status_code == 200:
                return response.json()  
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error in parsing email content: {e}")
            return None

    def extract_name_from_email(self, sender):
        match = re.match(r'([^<]*)<([^>]+)>', sender)
        if match:
            name = match.group(1).strip()  
            return name.split()[0]  
        else:
            return sender.split('@')[0]  

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailApp(root)
    root.mainloop()





