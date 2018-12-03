import web, importlib.util
# we have to do this stuff so python can find our modules since we use mod_wsgi
spec = importlib.util.spec_from_file_location('generate', '/var/www/projects.lucaslower.com/us-map/modules/generate.py')
generate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate)


# init rendering engine
render = web.template.render('/var/www/projects.lucaslower.com/us-map/views/')


# init routes
routes = (
    '/render', 'render_map',
    '/(.*)', 'index',
)


class index:
    """
    index class---handles initial options setup
    """
    def GET(self, name=None):
        return render.index(name)


class render_map:
    """
    render_map class---handles map render
    """
    def GET(self):
        # redirect to index
        raise web.redirect('/')

    # helper functions for map generation
    def POST(self):
        data = web.input()
        url = generate.generate_map(int(data['data_file']),str(data['start_color']),str(data['end_color']))
        return render.render(url)


# run app
application = web.application(routes, globals()).wsgifunc()