import json

from django.http import HttpResponse
from django.shortcuts import render
import shanxi_tourism.models as models
from django.http import HttpResponseNotFound
from django.db.models import Q


def get_attraction(request):
    """处理获取某个景点的请求
        0.调用check_login()函数验证登录
        1.首先从request中获取传递的参数: attraction_id
        2.从数据库中取出给定attraction_id的attraction实体
        3.从数据库中取出这个景点对应的酒店，若不够4个，则再取出热门酒店直到取出了4个酒店
        4.从数据库中取出这个景点对应的游记，若不够2个，则再取出热门游记直到取出了2个游记
        5.将attraction实体、酒店的列表和游记的列表放入ctx(context, 上下文中)
        6.通过render()函数将此次请求转发给视图层的attraction.html进行下一步处理
        :arg
            attraction_id: 这个景点的编号
    """
    ctx = {'active': 2}
    check_login(request, ctx)
    if request.GET:
        try:
            attraction_id = request.GET['attraction_id']
            attraction = models.Attraction.objects.get(attraction_id=attraction_id)
            ctx['attraction'] = attraction
            travels_list = []
            travels_list.extend(models.Travels.objects.filter(attraction_id=attraction_id))
            if len(travels_list) < 2:
                remain = 2 - len(travels_list)
                travels_list.extend(models.Travels.objects.order_by('travels_view_num').reverse()[0:remain])
            ctx['travels_list'] = travels_list
            print(type(travels_list))
            hotel_list = []
            hotel_list.extend(models.Hotel.objects.filter(attraction_id=attraction_id))
            if len(hotel_list) < 4:
                remain = 4 - len(hotel_list)
                hotel_list.extend(models.Hotel.objects.order_by('hotel_id')[0:remain])
            ctx['hotel_list'] = hotel_list
            print(type(hotel_list))
            return render(request, 'attraction.html', ctx)
        except Exception as e:
            return HttpResponseNotFound("页面不存在")


def get_travels(request):
    """处理获取某篇游记的请求
        0.调用check_login()函数验证登录
        1.首先从request中获取传递的参数: travels_id
        2.从数据库中取出给定travels_id的travels实体
        3.从数据库中取出此travels对应的attraction(景点)这一实体
        4.将景点实体和游记实体放入ctx(context, 上下文中)
        5.通过render()函数将此次请求转发给视图层的travels.html进行下一步处理
        :arg
            travels_id: 这篇游记的游记编号
    """
    ctx = {'active': 4}
    check_login(request, ctx)
    if request.GET:
        travels_id = request.GET['travels_id']
        travels = models.Travels.objects.get(travels_id=travels_id)
        ctx['travels'] = travels
        ctx['attraction'] = models.Attraction.objects.get(attraction_id=travels.attraction_id)
    return render(request, 'travels.html', ctx)


def get_hotel(request):
    """处理获取某个酒店的请求
        0.调用check_login()函数验证登录
        1.首先从request中获取传递的参数: hotel_id
        2.从数据库中取出给定hotel_id的hotel实体
        5.将hotel实体、放入ctx(context, 上下文中)
        6.通过render()函数将此次请求转发给视图层的hotel.html进行下一步处理
        :arg
            attraction_id: 这个景点的编号
    """
    ctx = {'active': 5}
    check_login(request, ctx)
    if request.GET:
        hotel_id = request.GET['hotel_id']
        hotel = models.Hotel.objects.get(hotel_id=hotel_id)
        ctx['hotel'] = hotel
        comments = []
        try:
            comments.extend(
                models.HotelComment.objects.filter(hotel_id=hotel_id).order_by("hotel_comment_date").reverse())
        except:
            pass
        ctx['comments'] = comments
        ctx['comments_empty'] = len(comments) == 0
    return render(request, 'hotel.html', ctx)


def get_route(request):
    """处理获取某个酒店的请求
        0.调用check_login()函数验证登录
        1.首先从request中获取传递的参数: route_id
        2.从数据库中取出给定route_id的route实体
        5.将route实体、放入ctx(context, 上下文中)
        6.通过render()函数将此次请求转发给视图层的route.html进行下一步处理
        :arg
            route_id: 这个自由行的编号
    """
    ctx = {'active': 6}
    check_login(request, ctx)
    if request.GET:
        route_id = request.GET['route_id']
        route = models.Route.objects.get(route_id=route_id)
        ctx['route'] = route
        comments = []
        try:
            comments.extend(models.RouteComment.objects.filter(route_id=route_id).order_by("route_comment_date").reverse())
        except:
            pass
        ctx['comments'] = comments
        ctx['comments_empty'] = len(comments) == 0
    return render(request, 'route.html', ctx)


def hot_attraction(request):
    """处理得到热门景点的请求
        0.验证是否登录
        1.从request上获得page参数(当前页码,从0开始)
        2.通过page参数算出现在需要第start到end条数据，其实end - start = 3
        3.到数据库中按照attraction_rank(景区排行)进行排序，并取出第start到第end条数据
        4.计算上一页和下一页的页码
        5.将数据通过render()函数发送给hot_attraction.html进行渲染
        :arg
            page: 本次的页码
    """
    ctx = {'active': 2}
    check_login(request, ctx)
    page = int(request.GET.get('page', default=0))
    results = []
    if page < 0:
        page = 0
    start = page * 3
    end = start + 3
    print(start)
    print(end)
    results.extend(models.Attraction.objects.order_by("attraction_rank")[start:end])
    ctx['results'] = adjust_rank(results)
    ctx['pre_page'] = max(page - 1, 0)
    ctx['next_page'] = page + 1
    return render(request, 'hot_attraction.html', ctx)


def hot_travels(request):
    """处理得到热门游记的请求
        0.验证是否登录
        1.从request上获得page参数(当前页码,从0开始)
        2.通过page参数算出现在需要第start到end条数据，其实end - start = 3
        3.到数据库中按照travels_view_num(游记观看数)进行排序，并取出第start到第end条数据
        4.计算上一页和下一页的页码
        5.将数据通过render()函数发送给hot_travels.html进行渲染
        :arg
            page: 本次的页码
    """
    ctx = {'active': 4}
    check_login(request, ctx)
    page = int(request.GET.get('page', default=0))
    results = []
    if page < 0:
        page = 0
    start = page * 3
    end = start + 3
    print(start)
    print(end)
    results.extend(models.Travels.objects.order_by("travels_view_num").reverse()[start:end])
    ctx['results'] = results
    ctx['pre_page'] = max(page - 1, 0)
    ctx['next_page'] = page + 1
    return render(request, 'hot_travels.html', ctx)


def hot_hotel(request):
    """处理得到热门酒店的请求
        与上两个方法的思路相同，请参见hot_travels的注释，自行领会
    """
    ctx = {'active': 5}
    check_login(request, ctx)
    page = int(request.GET.get('page', default=0))
    results = []
    if page < 0:
        page = 0
    start = page * 3
    end = start + 3
    print(start)
    print(end)
    results.extend(models.Hotel.objects.order_by("hotel_id")[start:end])
    ctx['results'] = results
    ctx['pre_page'] = max(page - 1, 0)
    ctx['next_page'] = page + 1
    return render(request, 'hot_hotel.html', ctx)


def hot_route(request):
    """处理得到热门旅游路线的请求
        与上三个方法的思路相同，请参见hot_travels的注释，自行领会
    """
    ctx = {'active': 6}
    check_login(request, ctx)
    page = int(request.GET.get('page', default=0))
    results = []
    if page < 0:
        page = 0
    start = page * 3
    end = start + 3
    print(start)
    print(end)
    results.extend(models.Route.objects.order_by("route_id")[start:end])
    ctx['results'] = results
    ctx['pre_page'] = max(page - 1, 0)
    ctx['next_page'] = page + 1
    return render(request, 'hot_route.html', ctx)


def route_search_result(request):
    """处理显示搜索结果的请求
        此界面上主要显示一个搜索框和对应关键字的搜索结果
        0.验证是否登录
        1.从request上获得s_str字段
        2.到数据库中通过对自由行的名称和标签进行子串匹配得到这个字段对应的多个自由行(注意，这里是名称和标签)
        3.将这些数据全部通过render()函数发送给search_result.html进行渲染
        :arg
            s_str: 本次搜索的关键字
    """
    ctx = {"active": 6}
    check_login(request, ctx)
    if request.GET:
        s_str = request.GET['s_str']
        results = []
        results.extend(models.Route.objects.
                       filter(Q(route_name__contains=s_str) | Q(route_tag__contains=s_str)).order_by("route_id"))
        ctx['is_empty'] = len(results) == 0
        ctx['s_str'] = s_str
        ctx['results'] = results
    return render(request, 'route_search_result.html', ctx)


def attraction_search_result(request):
    """处理显示景点搜索结果的请求
        此界面上主要显示一个搜索框和对应关键字的搜索结果
        0.验证是否登录
        1.从request上获得s_str字段
        2.到数据库中通过对景点的名称进行子串匹配得到这个字段对应的多个景点
        3.若已经登录则首先将本次搜索历史存储到数据库中，然后取出用户的最近5条搜索历史
        4.将这些数据全部通过render()函数发送给search_result.html进行渲染
        :arg
            s_str: 本次搜索的关键字
    """
    ctx = {'active': 2}
    check_login(request, ctx)
    if request.GET:
        s_str = request.GET['s_str']
        results = []
        results.extend(models.Attraction.objects.filter(attraction_name__contains=s_str).order_by("attraction_rank"))
        ctx['is_empty'] = len(results) == 0
        ctx['results'] = adjust_rank(results)
        ctx['s_str'] = s_str
    return render(request, 'attraction_search_result.html', ctx)


def hotel_search_result(request):
    """处理显示酒店搜索结果的请求
        与上一个函数逻辑相同
        但要注意: 这里是对旅馆的名称和旅馆的位置都进行了子串匹配，注意!!!!！
        :arg
            s_str: 本次搜索的关键字
    """
    ctx = {"active": 5}
    check_login(request, ctx)
    if request.GET:
        s_str = request.GET['s_str']
        results = []
        results.extend(models.Hotel.objects.
                       filter(Q(hotel_name__contains=s_str) | Q(hotel_position__contains=s_str)).order_by("hotel_id"))
        ctx['is_empty'] = len(results) == 0
        ctx['s_str'] = s_str
        ctx['results'] = results
    return render(request, 'hotel_search_result.html', ctx)


def travels_search_result(request):
    """处理显示游记搜索结果的请求
        与上一个函数逻辑相同
        :arg
            s_str: 本次搜索的关键字
    """
    ctx = {'active': 4}
    check_login(request, ctx)
    if request.GET:
        s_str = request.GET['s_str']
        results = []
        results.extend(models.Travels.objects
                       .filter(Q(travels_content_cut__contains=s_str) | Q(travels_name__contains=s_str))
                       .order_by("travels_view_num").reverse())
        ctx['is_empty'] = len(results) == 0
        ctx['s_str'] = s_str
        ctx['results'] = results
    return render(request, 'travels_search_result.html', ctx)


def comment_hotel(request):
    """处理对景点进行评论的请求
        0.首先从session中获取这次请求的用户信息，主要是用户的id
        1.然后提取POST报文中发来的数据,包括hotel_id、comment等
        2.用这些数据创建一个comment实体，并存储到数据库中
        3.若这些步骤未发生异常，则向客户端发送{OK:1},否则发送{OK:0}
        :arg
            hotel_id: 这个酒店的编号
            comment: comment的实际内容
    """
    user = request.session.get("user", None)
    user_id = None
    if user is not None:
        user_id = user.user_id
    print(request.POST)
    if request.POST:
        try:
            comment = models.HotelComment()
            comment.user_id = user_id
            comment.hotel_id = request.POST.get('hotel_id')
            comment.hotel_comment_content = request.POST.get("comment")
            comment.save()
            ok = 1
        except Exception as e:
            e.with_traceback()
            ok = 0
        data = {"ok": ok}
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


def comment_route(request):
    """处理对自由行进行评论的请求
        逻辑与上一个函数相同
        :arg
            hotel_id: 这个酒店的编号
            comment: comment的实际内容
    """
    user = request.session.get("user", None)
    user_id = None
    if user is not None:
        user_id = user.user_id
    print(request.POST)
    if request.POST:
        try:
            comment = models.RouteComment()
            comment.user_id = user_id
            comment.route_id = request.POST.get('route_id')
            comment.route_comment_content = request.POST.get("comment")
            comment.save()
            ok = 1
        except Exception as e:
            e.with_traceback()
            ok = 0
        data = {"ok": ok}
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


def order_route(request):
    """处理预定自由行的请求
        0.首先检查session中是否存在用户
        1.然后从POST报文的请求提取参数,例如:用户名、预定开始时间等
        2.用这些参数构建一个RouteOrder实体
        3.对这个实体进行数据库存储
        :arg
            hotel_id: 这个酒店的编号
            comment: comment的实际内容
    """
    user = request.session.get("user", None)
    user_id = None
    if user is not None:
        user_id = user.user_id
    print(request.POST)
    if request.POST:
        try:
            route_order = models.RouteOrder()
            route_order.name = request.POST.get("name")
            route_order.id_card = request.POST.get("id")
            route_order.tel_num = request.POST.get("tel")
            route_order.description = request.POST.get("desc")
            route_order.route_id = request.POST.get("route_id")
            route_order.user_id = user_id
            route_order.save()
            ok = 1
        except Exception as e:
            e.with_traceback()
            ok = 0
        data = {"ok": ok}
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


def delete_route_comment(request):
    if request.GET:
        try:
            data_id = request.GET.get("data_id")
            models.RouteComment.objects.get(route_comment_id=data_id).delete()
            ok = 1
        except Exception as e:
            e.with_traceback()
            ok = 0
        data = {"ok": ok}
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


def delete_hotel_comment(request):
    if request.GET:
        try:
            data_id = request.GET.get("data_id")
            models.HotelComment.objects.get(hotel_comment_id=data_id).delete()
            ok = 1
        except Exception as e:
            e.with_traceback()
            ok = 0
        data = {"ok": ok}
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


def delete_hotel_order(request):
    if request.GET:
        try:
            data_id = request.GET.get("data_id")
            models.HotelOrder.objects.get(hotel_order_id=data_id).delete()
            ok = 1
        except Exception as e:
            e.with_traceback()
            ok = 0
        data = {"ok": ok}
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


def delete_route_order(request):
    if request.GET:
        try:
            data_id = request.GET.get("data_id")
            models.RouteOrder.objects.get(route_order_id=data_id).delete()
            ok = 1
        except Exception as e:
            e.with_traceback()
            ok = 0
        data = {"ok": ok}
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


def my(request):
    ctx = {}
    check_login(request, ctx)
    if ctx['login']:
        user = request.session.get("user", None)
        hotel_comments = []
        hotel_comments.extend(models.HotelComment.objects.filter(user_id=user.user_id))
        ctx["hotel_comments"] = hotel_comments
        ctx["has_hotel_comments"] = len(hotel_comments) != 0
        route_comments = []
        route_comments.extend(models.RouteComment.objects.filter(user_id=user.user_id))
        ctx["route_comments"] = route_comments
        ctx["has_route_comments"] = len(route_comments) != 0
        hotel_orders = []
        hotel_orders.extend(models.HotelOrder.objects.filter(user_id=user.user_id))
        ctx["hotel_orders"] = hotel_orders
        ctx["has_hotel_order"] = len(hotel_orders) != 0
        route_orders = []
        route_orders.extend(models.RouteOrder.objects.filter(user_id=user.user_id))
        ctx["route_orders"] = route_orders
        ctx["has_route_order"] = len(route_orders) != 0
    return render(request, 'my.html', ctx)


def order_hotel(request):
    """处理预定的请求
        逻辑与上一个函数相同
        :arg
            hotel_id: 这个酒店的编号
            comment: comment的实际内容
    """
    print("here")
    user = request.session.get("user", None)
    user_id = None
    if user is not None:
        user_id = user.user_id
    print(request.POST)
    if request.POST:
        try:
            hotel_order = models.HotelOrder()
            hotel_order.name = request.POST.get("name")
            hotel_order.start_time = request.POST.get("start")
            hotel_order.end_time = request.POST.get("end")
            hotel_order.id_card = request.POST.get("id")
            hotel_order.tele_num = request.POST.get("tel")
            hotel_order.description = request.POST.get("des")
            hotel_order.hotel_id = request.POST.get("hotel_id")
            hotel_order.user_id = user_id
            hotel_order.hotel_type = request.POST.get("select")
            hotel_order.save()
            ok = 1
        except Exception as e:
            e.with_traceback()
            ok = 0
        data = {"ok": ok}
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


def index(request):
    """处理获取首页的请求
        首页中主要显示
            1.两个最热门的景点
            2.两篇最热门的游记
            3.四个最热门的酒店
        所以，大致上就是去数据库中找到这些数据
        然后，将其绑定到ctx上，通过render()转发给index,html进行渲染
    """
    ctx = {'active': 1}
    check_login(request, ctx)
    attraction_list = []
    attraction_list.extend(models.Attraction.objects.order_by("attraction_rank")[0:2])
    ctx['attraction_list'] = adjust_rank(attraction_list)
    travels_list = []
    travels_list.extend(models.Travels.objects.order_by('travels_view_num').reverse()[0:2])
    ctx['travels_list'] = travels_list
    hotel_list = []
    hotel_list.extend(models.Hotel.objects.order_by('hotel_id')[0:4])
    ctx['hotel_list'] = hotel_list
    return render(request, 'index.html', ctx)


def register(request):
    """处理注册请求
        用户在前端点击注册按钮，提交表单会触发这一请求
        这里实现的比较简单
            0.从request上获取email、password、nickname等参数
            1.用这几个参数构建一个user实体，调用这个实体将user进行到数据库的持久化存储(并没有进行数据的验证，(⊙﹏⊙)我给省略了)
            2.将请求重定向至首页，换言之，用户注册完成后，会跳转到首页(这里有点不人性化，但是也是为了省事)
        :arg
            email:
            password:
            nickname:
    """
    if request.GET:
        user = request.GET['email']
        password = request.GET['password']
        nickname = request.GET['nickname']
        print(user, password, nickname)
        ok = 1
        try:
            old_user = models.User.objects.get(user_id=user)
            ok = 0
        except Exception as e:
            user = models.User(user_id=user, user_nick=nickname, user_password=password)
            user.save()
            request.session['user'] = user
        data = {"ok": ok}
        data = json.dumps(data)
        print(data)
        return HttpResponse(data, content_type="application/json")


def login(request):
    """处理登录请求
        用户在前端点击登录按钮，提交表单会触发这一请求
        这里实现的同样比较简单
            0.从request上获取email、password、nickname等参数
            1.然后从数据库中取出对应email用户的密码
            2.将两个密码进行比较，若相同，则将用户实体(user)存储到本次session中
            3.将请求重定向至首页
        :arg
            email:
            password:
    """
    if request.GET:
        user = request.GET['email']
        password = request.GET['password']
        print(user, password)
        ok = 0
        try:
            user = models.User.objects.get(user_id=user)
            if password == user.user_password:
                request.session['user'] = user
                ok = 1
        except Exception as e:
            pass
        data = {"ok": ok}
        data = json.dumps(data)
        print(data)
        return HttpResponse(data, content_type="application/json")


def logout(request):
    """处理注销请求
        用户在前端点击标有"用户名称"和"注销"的按钮，提交表单会触发这一请求
        这里实现的同样比较简单
            0.检查session中是否绑定了用户
            1.若绑定，则将user解绑，即设为None
            2.通知前端刷新界面
        :arg
            email:
            password:
    """
    if request.session.get("user", None) is not None:
        request.session['user'] = None
    data = {"ok": 1}
    data = json.dumps(data)
    print(data)
    return HttpResponse(data, content_type="application/json")


def check_login(request, ctx):
    """验证登录
        这个函数并不处理任何请求，但它被上面大多数函数调用，用来验证用户是否登录
        0.首先检查session中是否有user这一实体
        1.若有，则在上下文(ctx)中加入login=True以说明已登录，并且前面得到的user实体也被加入到ctx中
        2.若无，则在上下文(ctx)中加入login=False以说明未登录
    """
    if request.session.get("user", None) is None:
        ctx['login'] = False
    else:
        ctx['login'] = True
        ctx['nickname'] = request.session.get("user", None).user_nick


def adjust_rank(attraction_list):
    for att in attraction_list:
        att.attraction_rank += 1
    return attraction_list
