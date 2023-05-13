from pyngrok import ngrok, conf, exception

def connect(token, port, region):
    account = None
    if token is None:
        token = 'None'
    else:
        if ':' in token:
            # token = authtoken:username:password
            account = token.split(':')[1] + ':' + token.split(':')[-1]
            token = token.split(':')[0]

    config = conf.PyngrokConfig(
        auth_token=token, region=region
    )
    
    # Guard for existing tunnels
    existing = ngrok.get_tunnels(pyngrok_config=config)
    if existing:
        for established in existing:
            # Extra configuration in the case that the user is also using ngrok for other tunnels
            if established.config['addr'][-4:] == str(port):
                public_url = existing[0].public_url
                print(f'ngrok has already been connected to localhost:{port}! URL: {public_url}\n'
                    'You can use this link after the launch is complete.')
                return
    
    try:
        if account is None:
            public_url = ngrok.connect(port, pyngrok_config=config, bind_tls=True).public_url
        else:
            public_url = ngrok.connect(port, pyngrok_config=config, bind_tls=True, auth=account).public_url
    except exception.PyngrokNgrokError:
        print('указан неверный токен или тебе выпал общий токен который использует другой анон, получи свежий: https://dashboard.ngrok.com/get-started/your-authtoken')
    else:
        print(f'\033[01;38;05;112m⯈\033[0m Ссылка на Нгрок: {public_url}')
