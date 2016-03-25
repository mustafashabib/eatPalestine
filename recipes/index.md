---
layout: page
title: Recipes
excerpt: "The recipes of EAT PALESTINE"
search_omit: true
---

<ul class="post-list">
{% for post in site.recipes %}
   <li><article><a href="{{ site.url }}{{ post.url }}">{{ post.title }} <span class="entry-date"></span>{% if post.excerpt %} <span class="excerpt">{{ post.excerpt | remove: '\[ ... \]' | remove: '\( ... \)' | markdownify | strip_html | strip_newlines | escape_once }}</span>{% endif %}</a></article></li>
{% endfor %}
</ul>
