import os
import pandas as pd
import re
from groq import Groq

# Set API key (biasanya disimpan sebagai environment variable)
api_key = os.environ.get("GROQ_API_KEY")

# Buat instance client Groq
client = Groq(api_key=api_key)

# Fungsi untuk membaca dan memparse file soal.txt
def read_transactions(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    transactions = []
    for line in lines[1:]:
        match = re.match(r'(\d+) Januari, (.+)', line.strip())
        if match:
            day = match.group(1)
            transaction = match.group(2)
            transactions.append((int(day), transaction))
    
    return transactions

# Fungsi untuk mengirim data transaksi ke Groq dan mendapatkan hasil
def get_financial_reports(transactions):
    transaction_texts = [f"{day} Januari: {transaction}" for day, transaction in transactions]
    prompt = (
        "Berikut adalah data transaksi:\n" + "\n".join(transaction_texts) +
        "\n\nBuatlah jurnal umum, buku besar, dan neraca saldo dari data di atas. "
        "Format hasil yang diinginkan adalah sebagai berikut:\n\n"
        "**General Journal**\n\n"
        "| Date | Account | Debit | Credit | Balance |\n"
        "| --- | --- | --- | --- | --- |\n"
        "**Ledger Accounts**\n\n"
        "**Cash**\n\n"
        "| Date | Debit | Credit | Balance |\n"
        "| --- | --- | --- | --- |\n"
        "**Accounts Payable**\n\n"
        "| Date | Debit | Credit | Balance |\n"
        "| --- | --- | --- | --- |\n"
        "**Accounts Receivable**\n\n"
        "| Date | Debit | Credit | Balance |\n"
        "| --- | --- | --- | --- |\n"
        "**Inventory**\n\n"
        "| Date | Debit | Credit | Balance |\n"
        "| --- | --- | --- | --- |\n"
        "**Balance Sheet**\n\n"
        "| Account | Debit | Credit | Balance |\n"
        "| --- | --- | --- | --- |\n"
    )
    
    print("Prompt yang dikirim ke Groq:")
    print(prompt)
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )

    result = chat_completion.choices[0].message.content
    print("Hasil dari Groq:")
    print(result)
    
    return result

# Fungsi untuk memparse hasil dari Groq menjadi DataFrame
def parse_groq_result(groq_result):
    sections = groq_result.split("\n\n")
    journal = []
    ledger = {}
    trial_balance = []

    current_section = None
    for section in sections:
        lines = section.split("\n")
        if "General Journal" in lines[0]:
            current_section = "Journal"
            continue
        elif "Ledger Accounts" in lines[0]:
            current_section = "Ledger"
            continue
        elif "Balance Sheet" in lines[0]:
            current_section = "Trial Balance"
            continue

        if current_section == "Journal":
            for line in lines[2:]:  # Skip header lines
                if line.strip() and "|" in line:
                    parts = [part.strip() for part in line.split("|")[1:-1]]
                    journal.append(parts)

        elif current_section == "Ledger":
            if "**" in lines[0]:
                account_name = lines[0].replace("**", "").strip()
                ledger_entries = []
                for line in lines[2:]:
                    if line.strip() and "|" in line:
                        parts = [part.strip() for part in line.split("|")[1:-1]]
                        ledger_entries.append(parts)
                ledger[account_name] = ledger_entries

        elif current_section == "Trial Balance":
            for line in lines[2:]:
                if line.strip() and "|" in line:
                    parts = [part.strip() for part in line.split("|")[1:-1]]
                    trial_balance.append(parts)

    journal_df = pd.DataFrame(journal, columns=["Tanggal", "Akun", "Debit", "Kredit", "Saldo"])
    ledger_dfs = {account: pd.DataFrame(entries, columns=["Tanggal", "Debit", "Kredit", "Saldo"]) for account, entries in ledger.items()}
    trial_balance_df = pd.DataFrame(trial_balance, columns=["Akun", "Debit", "Kredit", "Saldo"])

    return journal_df, ledger_dfs, trial_balance_df

# Fungsi untuk menyimpan data ke dalam file Excel
def save_to_excel(journal, ledger, trial_balance, file_path):
    with pd.ExcelWriter(file_path) as writer:
        journal.to_excel(writer, sheet_name="Jurnal Umum", index=False)
        for account, entries in ledger.items():
            if not entries.empty:
                sheet_name = f"Buku Besar - {account}"
                if len(sheet_name) > 31:
                    sheet_name = sheet_name[:31]
                entries.to_excel(writer, sheet_name=sheet_name, index=False)
        trial_balance.to_excel(writer, sheet_name="Neraca Saldo", index=False)

# Main program
if __name__ == "__main__":
    transactions = read_transactions('soal.txt')
    groq_result = get_financial_reports(transactions)
    journal_df, ledger_dfs, trial_balance_df = parse_groq_result(groq_result)
    save_to_excel(journal_df, ledger_dfs, trial_balance_df, 'output_pembukuan.xlsx')
