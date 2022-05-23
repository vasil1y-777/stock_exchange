from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from companies.forms import *
from companies.models import Company, Photo, Industry
from marketplace.models import Shares
from rating.models import Rating


def get_dict_of_sorted_companies_by_industry():
    companies = Company.companies.get_sorted_companies_by_industry().all()

    industry_sort = dict()
    for company in companies:
        if company.industry in industry_sort:
            industry_sort[company.industry].append(company)
        else:
            industry_sort[company.industry] = [company]

    return industry_sort


class CompaniesView(View):
    template = 'companies/companies.html'
    form = ChangeTrustPointsForm

    def get(self, request):
        form = self.form()

        industry_sort = get_dict_of_sorted_companies_by_industry()

        context = {'companies_by_industry': industry_sort, 'form': form}
        return render(request, self.template, context)

    def post(self, request):
        form = self.form(request.POST)
        user = request.user
        user_rating = Rating.rating.filter(user=user).all()
        context = {'form': form}
        if form.is_valid():
            to_delete = list()  # temporary arrays for checking 100 points in each industry
            to_save = list()
            to_create = list()

            industries_names = Industry.industries.values_list('name', flat=True)
            industries = dict()
            for industry in industries_names:
                industries.update({industry: 0})

            for company, trust_points in form.cleaned_data.items():
                if trust_points >= 0:

                    company_name = " ".join(company.split('_')[1:])
                    company = Company.companies.filter(name=company_name).select_related('industry').first()
                    current_rating = user_rating.filter(user=user, company=company).first()

                    if trust_points == 0 and current_rating:
                        to_delete.append(current_rating)

                    elif trust_points == 0:
                        pass

                    elif current_rating:
                        industries[company.industry.name] += current_rating.points
                        current_rating.points = trust_points
                        to_save.append(current_rating)

                    else:
                        industries[company.industry.name] += trust_points
                        to_create.append({'company': company, 'points': trust_points, 'user': user})

            for trust_points_one_industry in industries.values():
                if trust_points_one_industry > 100:
                    return HttpResponseRedirect(reverse('companies'))

            for current_rating in to_delete:
                current_rating.delete()

            for current_rating in to_save:
                current_rating.save()

            for current_rating in to_create:
                Rating.rating.create(**current_rating).save()

            return HttpResponseRedirect(reverse('companies'))
        return render(request, self.template, context)


class CompanyView(View):
    template = 'companies/company.html'

    def get(self, request, company_name):
        company = (
            Company.companies.filter(name=company_name)
            .select_related('industry')
            .only('name', 'industry__name', 'description', 'upload')
            .first()
        )
        photos = Photo.objects.filter(company=company, is_active=True).all()
        context = {
            'company': company,
            'stockholders': Shares.shares.get_company_stockholders(company),
            'photos': photos,
        }
        return render(request, self.template, context)


class NewCompanyView(View):
    template = 'companies/new_company.html'
    form = NewCompanyForm

    def get(self, request):
        form = self.form()
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        def save_photo(photo, company):
            Photo.objects.create(upload=photo, company=company).save()

        form = self.form(request.POST, request.FILES)
        context = {'form': form}
        if form.is_valid():
            user = request.user
            if user.balance >= 500:
                user.balance -= 500
                user.save()
            else:
                form.add_error('name', 'У вас недостаточно средств')
                return render(request, self.template, context)

            company = Company.companies.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                industry=form.cleaned_data['industry'],
                upload=form.cleaned_data['logo'],
            )
            if form.cleaned_data['photo1']:
                save_photo(form.cleaned_data['photo1'], company)
            if form.cleaned_data['photo2']:
                save_photo(form.cleaned_data['photo2'], company)
            if form.cleaned_data['photo3']:
                save_photo(form.cleaned_data['photo3'], company)
            company.save()

            return HttpResponseRedirect(
                reverse('company', kwargs={'company_name': form.cleaned_data['name']}))
        return render(request, self.template, context)
