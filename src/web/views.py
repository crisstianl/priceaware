from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .forms import StoreForm, SearchForm, ItemForm
from persistence.daos import StoreDAO, ItemDAO, drop_db
from persistence.models import Store, Item
from api.crawlers import factory 
from concurrent.futures import ThreadPoolExecutor

def index(request, *args, **kwargs):
    print("REQUEST/index")
    return search(request, args, kwargs)

def stores(request, *args, **kwargs):
    print("REQUEST/stores:", request)
    print("ARGS:", args)
    print("KWARGS:", kwargs)

    # create page attributes 
    my_context = {}
    storeDAO = StoreDAO()

    if "GET" == request.method:
        if "q" in request.GET:
            my_form = SearchForm(request.GET or None)
            if my_form.is_valid():
                my_context["store_list"] = storeDAO.query_by_name(my_form.cleaned_data["q"])
            else:
                my_context["error_list"] = as_str(my_form.errors)
        else:
            my_context["store_list"] = storeDAO.query_all()

    elif "POST" == request.method:
        # create or update
        my_store = None
        my_store_id = request.POST.get('id')
        if my_store_id:
            my_store = storeDAO.query_by_id(my_store_id)

        my_form = StoreForm(request.POST or None, instance=my_store)
        if my_form.is_valid(): # trigger form validation and model validation        
            my_form.save(commit=True) # save or update

        else:
            my_context["error_list"] = as_str(my_form.errors)

        my_context["store_list"] = storeDAO.query_all()

    # HttpResponse
    return render(request, "index.html", my_context)

def search(request, *args, **kwargs):
    print("REQUEST/search:", request)
    print("ARGS:", args)
    print("KWARGS:", kwargs)

    # create page attributes 
    my_context = {}
    storeDAO = StoreDAO()

    if "GET" == request.method:
        if "q" in request.GET: 
            q_results = list()
            q_str = request.GET.get('q')
          
            # create crawlers
            crawlers = list()
            for store in storeDAO.query_all(0, 100):            
                crawler = factory(store, q_str)
                if crawler: crawlers.append(crawler) 

            # push result in context list
            def callback(name, link, price, store):
                q_item = Item(name=name, link=link, price=price, store=store)
                q_results.append(q_item)

            # execute each scrape in a separate thread
            with ThreadPoolExecutor(max_workers = len(crawlers)) as exec:
                for crawler in crawlers:
                    exec.submit(crawler.run, callback)

            # scrapping completed, sort results
            q_results.sort(reverse=True, key = lambda e : e.store.rating)

            my_context["item_list"] = q_results
            add_search_history(request, q_str) 
        
        # HttpResponse
        return render(request, "prices.html", my_context)

    elif "POST" == request.method:
        # need to set store from request store_id
        my_form = ItemForm(request.POST or None)
        if my_form.is_valid(): # trigger form validation and model validation  
            my_item = my_form.save(commit=False) # don't flush to DB
            my_store = Store()
            my_store.id = my_form.cleaned_data['store_id']
            my_item.store = my_store
            my_item.save() # flush into DB
            
            # HttpResponse
            return HttpResponse(status=201)
        else:
            print(my_form.errors)
            # HttpResponse
            return HttpResponse(status=400)

def delete(request, *args, **kwargs):
    print("REQUEST/delete:", request)
    print("ARGS:", args)
    print("KWARGS:", kwargs)

    storeDAO = StoreDAO()
    if "POST" == request.method:
        if "id" in request.POST:
            my_store_id = request.POST.get('id')
            storeDAO.delete_by_id(my_store_id)

    return redirect(reverse("web:stores"))

def cart(request, *args, **kwargs):
    print("REQUEST/delete:", request)
    print("ARGS:", args)
    print("KWARGS:", kwargs)

    # create page attributes 
    my_context = {}
    itemDAO = ItemDAO()

    if "GET" == request.method:
        my_context["item_list"] = itemDAO.query_all()

        # HttpResponse
        return render(request, "cart.html", my_context)

    elif "POST" == request.method:
        itemDAO.delete_by_id(request.POST.get('id'))
        return HttpResponse(status=200)

def settings(request, *args, **kwargs):
    print("REQUEST/delete:", request)
    print("ARGS:", args)
    print("KWARGS:", kwargs)

    # create page attributes 
    my_context = {}

    if "GET" == request.method:
        # HttpResponse
        return render(request, "settings.html", my_context)

    elif "POST" == request.method:
        storeDAO = StoreDAO()
        itemDAO = ItemDAO()

        action = request.POST.get('action')
        if not action:
            return HttpResponse(status=400)

        if "del_cart" == action:
            itemDAO.delete_all()
            return HttpResponse(status=200)

        elif "del_store" == action:
            storeDAO.delete_all()
            return HttpResponse(status=200)

        elif "def_db" == action:
            drop_db()
            return HttpResponse(status=200)
        
def as_str(formErrors):
    str = ""
    for key,value in formErrors.items():
        str += value
    return str

def add_search_history(request, value):
    if "search_history" in request.session:
        request.session['search_history'].append(value)
    else:
        request.session['search_history'] = [value, ]
    
