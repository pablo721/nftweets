from django.shortcuts import render
from django.views.generic import TemplateView


class PopularView(TemplateView):
    template_name = 'mood/popular.html'


class SpecificView(TemplateView):
    template_name = 'mood/specific.html'


class SpacesView(TemplateView):
    template_name = 'mood/spaces.html'


class InfluencersView(TemplateView):
    template_name = 'mood/influencers.html'


class MentionsView(TemplateView):
    template_name = 'mood/mentions.html'

    def get(self, request, *args, **kwargs):
        context = {}
        if 'query' in str(request.GET):
            context = self.get_context_data(query=request.GET.get('query'), granularity=request.GET.get('granularity'))
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        query = kwargs['query']
        granularity = kwargs['granularity']
        df = tweet_count({'query': query, 'granularity': granularity})
        chart = Chart('line', chart_id='mentions_chart', palette=[get_random_color() for col in df.columns])
        chart.from_df(df, values=['mentions'], labels='start')

        return {'query': query, 'granularity': granularity, 'start_date': df.loc[0, 'start'],
                'end_date': df['end'].values[-1], 'total_count': sum(df['mentions']),
                'table': table.to_html(escape=False, justify='center'), 'chart': chart.get_html(),
                'js_scripts': chart.get_js()}


