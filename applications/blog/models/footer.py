# -*- coding: utf-8 -*-

latest_posts = db(Posts).select(orderby=~Posts.created_on, limitby=(0,5))
most_liked = db(Posts).select(orderby=~Posts.likes, limitby=(0,5))
all_categories = db(Categories).select(limitby=(0,5))