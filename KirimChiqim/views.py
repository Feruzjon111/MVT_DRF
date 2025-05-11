from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm, DateRangeForm
from datetime import timedelta
from django.utils.timezone import now
from django.utils.translation import gettext as _

def my_view(request):
    greeting = _("Welcome to your income and expense tracker.")
    return HttpResponse(greeting)


@login_required
def index(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date')

    total_income = 0
    total_expense = 0

    income_transactions = transactions.filter(type='IN')
    for transaction in income_transactions:
        if transaction.valyuta_turi == 'USD':
            total_income += transaction.amount * 13000
        elif transaction.valyuta_turi == 'EUR':
            total_income += transaction.amount * 14500
        elif transaction.valyuta_turi == 'RUB':
            total_income += transaction.amount * 160
        else:
            total_income += transaction.amount

    expense_transactions = transactions.filter(type='OUT')
    for transaction in expense_transactions:
        if transaction.valyuta_turi == 'USD':
            total_expense += transaction.amount * 13000
        elif transaction.valyuta_turi == 'EUR':
            total_expense += transaction.amount * 14500
        elif transaction.valyuta_turi == 'RUB':
            total_expense += transaction.amount * 160
        else:
            total_expense += transaction.amount

    balance = total_income - total_expense

    category_expenses = (
        Transaction.objects
        .filter(user=user, type='OUT')
        .values('category', 'valyuta_turi')
        .annotate(total_amount=Sum('amount'))
        .order_by('category')
    )

    lst = []
    for expense in category_expenses:
        if expense['valyuta_turi'] == 'USD':
            exchange_rate = 13000
            total_amount_in_som = expense['total_amount'] * exchange_rate
        elif expense['valyuta_turi'] == 'EUR':
            exchange_rate = 14500
            total_amount_in_som = expense['total_amount'] * exchange_rate
        elif expense['valyuta_turi'] == 'RUB':
            exchange_rate = 160
            total_amount_in_som = expense['total_amount'] * exchange_rate
        elif expense['valyuta_turi'] == 'Karta':
            total_amount_in_som = expense['total_amount']
        else:
            total_amount_in_som = expense['total_amount']
        lst.append({
            'category': expense['category'],
            'total_amount_in_som': total_amount_in_som
        })

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'category_expenses': lst,
    }
    return render(request, 'index.html', context)


@login_required
def add_transaction(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)
    total_income = transactions.filter(type='IN').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(type='OUT').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            if transaction.type == 'OUT' and transaction.amount > balance:
                return render(request, 'add_transaction.html', {'form': form, 'error_message': 'Balansingiz yetarli emas. Iltimos, balansingizni to\'ldiring.'})
            transaction.save()
            return redirect('index')
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})


@login_required
def reports(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)
    # total_income = sum(t.amount for t in transactions if t.type == 'IN')
    # total_expense = sum(t.amount for t in transactions if t.type == 'OUT')
    # balance = total_income - total_expense
    total_income = 0
    total_expense = 0

    income_transactions = transactions.filter(type='IN')
    for transaction in income_transactions:
        if transaction.valyuta_turi == 'USD':
            total_income += transaction.amount * 13000
        elif transaction.valyuta_turi == 'EUR':
            total_income += transaction.amount * 14500
        elif transaction.valyuta_turi == 'RUB':
            total_income += transaction.amount * 160
        else:
            total_income += transaction.amount

    expense_transactions = transactions.filter(type='OUT')
    for transaction in expense_transactions:
        if transaction.valyuta_turi == 'USD':
            total_expense += transaction.amount * 13000
        elif transaction.valyuta_turi == 'EUR':
            total_expense += transaction.amount * 14500
        elif transaction.valyuta_turi == 'RUB':
            total_expense += transaction.amount * 160
        else:
            total_expense += transaction.amount

    balance = total_income - total_expense

    category_expenses = (
        Transaction.objects
        .filter(user=user, type='OUT')
        .values('category', 'valyuta_turi')
        .annotate(total_amount=Sum('amount'))
        .order_by('category')
    )

    lst = []
    for expense in category_expenses:
        if expense['valyuta_turi'] == 'USD':
            exchange_rate = 13000
            total_amount_in_som = expense['total_amount'] * exchange_rate
        elif expense['valyuta_turi'] == 'EUR':
            exchange_rate = 14500
            total_amount_in_som = expense['total_amount'] * exchange_rate
        elif expense['valyuta_turi'] == 'RUB':
            exchange_rate = 160
            total_amount_in_som = expense['total_amount'] * exchange_rate
        elif expense['valyuta_turi'] == 'Karta':
            total_amount_in_som = expense['total_amount']
        else:
            total_amount_in_som = expense['total_amount']
        lst.append({
            'category': expense['category'],
            'total_amount_in_som': total_amount_in_som
        })
    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    }
    return render(request, 'reports.html', context)


@login_required
def transactions_by_date_range(request):
    user = request.user
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        try:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)

            if start_date and end_date and start_date <= end_date:
                transactions = Transaction.objects.filter(user=user, date__range=[start_date, end_date])

                total_income = 0
                total_expense = 0

                income_transactions = transactions.filter(type='IN')
                for transaction in income_transactions:
                    if transaction.valyuta_turi == 'USD':
                        total_income += transaction.amount * 13000
                    elif transaction.valyuta_turi == 'EUR':
                        total_income += transaction.amount * 14500
                    elif transaction.valyuta_turi == 'RUB':
                        total_income += transaction.amount * 160
                    else:
                        total_income += transaction.amount

                expense_transactions = transactions.filter(type='OUT')
                for transaction in expense_transactions:
                    if transaction.valyuta_turi == 'USD':
                        total_expense += transaction.amount * 13000
                    elif transaction.valyuta_turi == 'EUR':
                        total_expense += transaction.amount * 14500
                    elif transaction.valyuta_turi == 'RUB':
                        total_expense += transaction.amount * 160
                    else:
                        total_expense += transaction.amount

                balance = total_income - total_expense

            else:
                transactions = []
                total_income = total_expense = balance = 0

        except ValueError:
            transactions = []
            total_income = total_expense = balance = 0
    else:
        transactions = []
        total_income = total_expense = balance = 0

    category_expenses = (
        Transaction.objects
        .filter(type='OUT')
        .values('category', 'valyuta_turi')
        .annotate(total_amount=Sum('amount'))
        .order_by('category')
    )

    categorized_expenses = []
    for expense in category_expenses:
        if expense['valyuta_turi'] == 'USD':
            exchange_rate = 13000
            total_amount_in_som = expense['total_amount'] * exchange_rate
        elif expense['valyuta_turi'] == 'EUR':
            exchange_rate = 14500
            total_amount_in_som = expense['total_amount'] * exchange_rate
        elif expense['valyuta_turi'] == 'RUB':
            exchange_rate = 160
            total_amount_in_som = expense['total_amount'] * exchange_rate
        else:
            total_amount_in_som = expense['total_amount']
        categorized_expenses.append({
            'category': expense['category'],
            'total_amount_in_som': total_amount_in_som
        })

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'category_expenses': categorized_expenses,
        'form': DateRangeForm(initial={'start_date': start_date_str, 'end_date': end_date_str}),
    }
    return render(request, 'kalendar.html', context)


@login_required
def daily_stats(request):
    user = request.user
    today = now().date()
    start_of_day = today
    end_of_day = start_of_day + timedelta(days=1)

    daily_income = Transaction.objects.filter(
        user=user, type='IN', date__range=[start_of_day, end_of_day]
    ).aggregate(total_income=Sum('amount'))['total_income'] or 0

    daily_expense = Transaction.objects.filter(
        user=user, type='OUT', date__range=[start_of_day, end_of_day]
    ).aggregate(total_expense=Sum('amount'))['total_expense'] or 0

    daily_transactions = Transaction.objects.filter(
        user=user, date__range=[start_of_day, end_of_day]
    ).values('type', 'amount', 'description', 'date')

    return JsonResponse({
        'daily_income': daily_income,
        'daily_expense': daily_expense,
        'daily_transactions': list(daily_transactions)
    })

@login_required
def weekly_stats(request):
    user = request.user
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)

    weekly_income = Transaction.objects.filter(
        user=user, type='IN', date__range=[start_of_week, end_of_week]
    ).aggregate(total_income=Sum('amount'))['total_income'] or 0

    weekly_expense = Transaction.objects.filter(
        user=user, type='OUT', date__range=[start_of_week, end_of_week]
    ).aggregate(total_expense=Sum('amount'))['total_expense'] or 0

    weekly_transactions = Transaction.objects.filter(
        user=user, date__range=[start_of_week, end_of_week]
    ).values('type', 'amount', 'description', 'date')

    return JsonResponse({
        'weekly_income': weekly_income,
        'weekly_expense': weekly_expense,
        'weekly_transactions': list(weekly_transactions)
    })


@login_required
def monthly_stats(request):
    user = request.user
    today = now().date()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=31)).replace(day=1)

    monthly_income = Transaction.objects.filter(
        user=user, type='IN', date__range=[start_of_month, end_of_month]
    ).aggregate(total_income=Sum('amount'))['total_income'] or 0

    monthly_expense = Transaction.objects.filter(
        user=user, type='OUT', date__range=[start_of_month, end_of_month]
    ).aggregate(total_expense=Sum('amount'))['total_expense'] or 0

    monthly_transactions = Transaction.objects.filter(
        user=user, date__range=[start_of_month, end_of_month]
    ).values('type', 'amount', 'description', 'date')

    return JsonResponse({
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'monthly_transactions': list(monthly_transactions)
    })

