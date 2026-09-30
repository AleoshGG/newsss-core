INFO:     Will watch for changes in these directories: ['/home/aleosh/Documentos/Jobs/Neurotry/newsss-core']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [135555] using WatchFiles
INFO:     Started server process [135558]
INFO:     Waiting for application startup.
[09/30/26 13:43:51] INFO     StreamableHTTP session manager started                                                                               streamable_http_manager.py:162
INFO:     Application startup complete.
INFO:     127.0.0.1:51074 - "POST /mcp HTTP/1.1" 307 Temporary Redirect
2026-09-30 13:43:55,526 INFO sqlalchemy.engine.Engine select pg_catalog.version()
[09/30/26 13:43:55] INFO     select pg_catalog.version()                                                                                                            base.py:1822
2026-09-30 13:43:55,528 INFO sqlalchemy.engine.Engine [raw sql] ()
                    INFO     [raw sql] ()                                                                                                                           base.py:1822
2026-09-30 13:43:55,772 INFO sqlalchemy.engine.Engine select current_schema()
                    INFO     select current_schema()                                                                                                                base.py:1822
2026-09-30 13:43:55,774 INFO sqlalchemy.engine.Engine [raw sql] ()
                    INFO     [raw sql] ()                                                                                                                           base.py:1822
2026-09-30 13:43:56,108 INFO sqlalchemy.engine.Engine show standard_conforming_strings
[09/30/26 13:43:56] INFO     show standard_conforming_strings                                                                                                       base.py:1822
2026-09-30 13:43:56,110 INFO sqlalchemy.engine.Engine [raw sql] ()
                    INFO     [raw sql] ()                                                                                                                           base.py:1822
2026-09-30 13:43:56,359 INFO sqlalchemy.engine.Engine BEGIN (implicit)
                    INFO     BEGIN (implicit)                                                                                                                       base.py:2679
2026-09-30 13:43:56,377 INFO sqlalchemy.engine.Engine SELECT youtube_videos.id, youtube_videos.title, youtube_videos.channel, youtube_videos.published_at, youtube_videos.url, youtube_videos.thumbnail_url, youtube_videos.transcript, youtube_videos.is_processed, youtube_videos.views, youtube_videos.likes, youtube_videos.comments 
FROM youtube_videos 
WHERE youtube_videos.is_processed = false ORDER BY youtube_videos.published_at DESC 
 LIMIT $1::INTEGER
                    INFO     SELECT youtube_videos.id, youtube_videos.title, youtube_videos.channel, youtube_videos.published_at, youtube_videos.url,               base.py:1822
                             youtube_videos.thumbnail_url, youtube_videos.transcript, youtube_videos.is_processed, youtube_videos.views, youtube_videos.likes,                  
                             youtube_videos.comments                                                                                                                            
                             FROM youtube_videos                                                                                                                                
                             WHERE youtube_videos.is_processed = false ORDER BY youtube_videos.published_at DESC                                                                
                              LIMIT $1::INTEGER                                                                                                                                 
2026-09-30 13:43:56,379 INFO sqlalchemy.engine.Engine [generated in 0.00197s] (50,)
                    INFO     [generated in 0.00197s] (50,)                                                                                                          base.py:1822
2026-09-30 13:43:56,380 INFO sqlalchemy.engine.Engine BEGIN (implicit)
                    INFO     BEGIN (implicit)                                                                                                                       base.py:2679
2026-09-30 13:43:56,382 INFO sqlalchemy.engine.Engine SELECT github_data.id, github_data.name, github_data.full_name, github_data.html_url, github_data.description, github_data.stargazers_count, github_data.language, github_data.updated_at, github_data.topics, github_data.readme, github_data.owner_avatar_url, github_data.forks_count, github_data.open_issues_count, github_data.license, github_data.is_processed 
FROM github_data 
WHERE github_data.is_processed = false ORDER BY github_data.updated_at DESC 
 LIMIT $1::INTEGER
                    INFO     SELECT github_data.id, github_data.name, github_data.full_name, github_data.html_url, github_data.description,                         base.py:1822
                             github_data.stargazers_count, github_data.language, github_data.updated_at, github_data.topics, github_data.readme,                                
                             github_data.owner_avatar_url, github_data.forks_count, github_data.open_issues_count, github_data.license, github_data.is_processed                
                             FROM github_data                                                                                                                                   
                             WHERE github_data.is_processed = false ORDER BY github_data.updated_at DESC                                                                        
                              LIMIT $1::INTEGER                                                                                                                                 
2026-09-30 13:43:56,384 INFO sqlalchemy.engine.Engine [generated in 0.00154s] (50,)
                    INFO     [generated in 0.00154s] (50,)                                                                                                          base.py:1822
2026-09-30 13:43:56,385 INFO sqlalchemy.engine.Engine BEGIN (implicit)
                    INFO     BEGIN (implicit)                                                                                                                       base.py:2679
2026-09-30 13:43:56,386 INFO sqlalchemy.engine.Engine SELECT google_news_articles.id, google_news_articles.title, google_news_articles.link, google_news_articles.pub_date, google_news_articles.source_name, google_news_articles.source_url, google_news_articles.fetched_at, google_news_articles.image_url, google_news_articles.content, google_news_articles.is_processed 
FROM google_news_articles 
WHERE google_news_articles.is_processed = false ORDER BY google_news_articles.fetched_at DESC 
 LIMIT $1::INTEGER
                    INFO     SELECT google_news_articles.id, google_news_articles.title, google_news_articles.link, google_news_articles.pub_date,                  base.py:1822
                             google_news_articles.source_name, google_news_articles.source_url, google_news_articles.fetched_at, google_news_articles.image_url,                
                             google_news_articles.content, google_news_articles.is_processed                                                                                    
                             FROM google_news_articles                                                                                                                          
                             WHERE google_news_articles.is_processed = false ORDER BY google_news_articles.fetched_at DESC                                                      
                              LIMIT $1::INTEGER                                                                                                                                 
2026-09-30 13:43:56,388 INFO sqlalchemy.engine.Engine [generated in 0.00178s] (50,)
                    INFO     [generated in 0.00178s] (50,)                                                                                                          base.py:1822
[09/30/26 13:43:57] INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    WARNING  Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we recommend to use AFC in    models.py:6228
                             Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend to use                 
                             AFC in Chat.send_message_stream.                                                                                                                   
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
[09/30/26 13:43:58] INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
[09/30/26 13:43:59] INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
[09/30/26 13:44:00] INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
[09/30/26 13:44:04] INFO     No device provided, using cpu                                                                                                          model.py:199
                    INFO     HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/modules.json "HTTP/1.1 307 Temporary  _client.py:1025
                             Redirect"                                                                                                                                          
                    INFO     HTTP Request: HEAD                                                                                                                  _client.py:1025
                             https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/mod                
                             ules.json?%2Fsentence-transformers%2Fall-MiniLM-L6-v2%2Fresolve%2Fmain%2Fmodules.json=&etag=%22952a9b81c0bfd99800fabf352f69c7ccd46c                
                             5e43%22 "HTTP/1.1 200 OK"                                                                                                                          
                    INFO     HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config_sentence_transformers.json     _client.py:1025
                             "HTTP/1.1 307 Temporary Redirect"                                                                                                                  
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
                    WARNING  Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster         _http.py:993
                             downloads.                                                                                                                                         
[09/30/26 13:44:05] INFO     HTTP Request: HEAD                                                                                                                  _client.py:1025
                             https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/con                
                             fig_sentence_transformers.json?%2Fsentence-transformers%2Fall-MiniLM-L6-v2%2Fresolve%2Fmain%2Fconfig_sentence_transformers.json=&et                
                             ag=%22fd1b291129c607e5d49799f87cb219b27f98acdf%22 "HTTP/1.1 200 OK"                                                                                
                    INFO     Loading SentenceTransformer model from sentence-transformers/all-MiniLM-L6-v2.                                                        model.py:1080
                    INFO     HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config_sentence_transformers.json     _client.py:1025
                             "HTTP/1.1 307 Temporary Redirect"                                                                                                                  
                    INFO     HTTP Request: HEAD                                                                                                                  _client.py:1025
                             https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/con                
                             fig_sentence_transformers.json?%2Fsentence-transformers%2Fall-MiniLM-L6-v2%2Fresolve%2Fmain%2Fconfig_sentence_transformers.json=&et                
                             ag=%22fd1b291129c607e5d49799f87cb219b27f98acdf%22 "HTTP/1.1 200 OK"                                                                                
                    INFO     HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/README.md "HTTP/1.1 307 Temporary     _client.py:1025
                             Redirect"                                                                                                                                          
                    INFO     HTTP Request: HEAD                                                                                                                  _client.py:1025
                             https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/REA                
                             DME.md?%2Fsentence-transformers%2Fall-MiniLM-L6-v2%2Fresolve%2Fmain%2FREADME.md=&etag=%2244af2e3b0fa3a0b6239e48422972bf755f28fde0%2                
                             2 "HTTP/1.1 200 OK"                                                                                                                                
                    INFO     HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/modules.json "HTTP/1.1 307 Temporary  _client.py:1025
                             Redirect"                                                                                                                                          
                    INFO     HTTP Request: HEAD                                                                                                                  _client.py:1025
                             https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/mod                
                             ules.json?%2Fsentence-transformers%2Fall-MiniLM-L6-v2%2Fresolve%2Fmain%2Fmodules.json=&etag=%22952a9b81c0bfd99800fabf352f69c7ccd46c                
                             5e43%22 "HTTP/1.1 200 OK"                                                                                                                          
                    INFO     HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/sentence_bert_config.json "HTTP/1.1   _client.py:1025
                             307 Temporary Redirect"                                                                                                                            
                    INFO     HTTP Request: HEAD                                                                                                                  _client.py:1025
                             https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/sen                
                             tence_bert_config.json?%2Fsentence-transformers%2Fall-MiniLM-L6-v2%2Fresolve%2Fmain%2Fsentence_bert_config.json=&etag=%2259d594003b                
                             f59880a884c574bf88ef7555bb0202%22 "HTTP/1.1 200 OK"                                                                                                
                    INFO     HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/adapter_config.json "HTTP/1.1 404 Not _client.py:1025
                             Found"                                                                                                                                             
                    INFO     HTTP Request: GET https://huggingface.co/api/models/sentence-transformers/all-MiniLM-L6-v2 "HTTP/1.1 200 OK"                        _client.py:1025
                    INFO     HTTP Request: GET https://huggingface.co/api/models/sentence-transformers/all-MiniLM-L6-v2 "HTTP/1.1 200 OK"                        _client.py:1025
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Translation error (lang=es): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Loading weights:   0%|          | 0/103 [00:00<?, ?it/s]Loading weights: 100%|██████████| 103/103 [00:00<00:00, 11327.04it/s]
[09/30/26 13:44:06] INFO     HTTP Request: GET https://huggingface.co/api/models/sentence-transformers/all-MiniLM-L6-v2 "HTTP/1.1 200 OK"                        _client.py:1025
                    INFO     HTTP Request: GET                                                                                                                   _client.py:1025
                             https://huggingface.co/api/models/sentence-transformers/all-MiniLM-L6-v2/tree/main/additional_chat_templates?recursive=false&expand                
                             =false "HTTP/1.1 404 Not Found"                                                                                                                    
                    INFO     HTTP Request: GET https://huggingface.co/api/models/sentence-transformers/all-MiniLM-L6-v2/tree/main?recursive=true&expand=false    _client.py:1025
                             "HTTP/1.1 200 OK"                                                                                                                                  
                    INFO     HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/1_Pooling/config.json "HTTP/1.1 307   _client.py:1025
                             Temporary Redirect"                                                                                                                                
                    INFO     HTTP Request: HEAD                                                                                                                  _client.py:1025
                             https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/1_P                
                             ooling%2Fconfig.json?%2Fsentence-transformers%2Fall-MiniLM-L6-v2%2Fresolve%2Fmain%2F1_Pooling%2Fconfig.json=&etag=%22d1514c3162bbe8                
                             7b343f565fadc62e6c06f04f03%22 "HTTP/1.1 200 OK"                                                                                                    
                    INFO     HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/2_Normalize/config.json "HTTP/1.1 404 _client.py:1025
                             Not Found"                                                                                                                                         
                    INFO     HTTP Request: GET https://huggingface.co/api/models/sentence-transformers/all-MiniLM-L6-v2 "HTTP/1.1 200 OK"                        _client.py:1025
2026-09-30 13:44:07,540 INFO sqlalchemy.engine.Engine BEGIN (implicit)
[09/30/26 13:44:07] INFO     BEGIN (implicit)                                                                                                                       base.py:2679
2026-09-30 13:44:07,544 INFO sqlalchemy.engine.Engine INSERT INTO content_clusters (topic_label, keywords, sources, avg_engagement_score, item_ids) SELECT p0::VARCHAR, p1::VARCHAR[], p2::VARCHAR[], p3::FLOAT, p4::VARCHAR[] FROM (VALUES ($1::VARCHAR, $2::VARCHAR[], $3::VARCHAR[], $4::FLOAT, $5::VARCHAR[] ... 371 characters truncated ... sen_counter RETURNING content_clusters.id, content_clusters.created_at, content_clusters.id AS id__1
                    INFO     INSERT INTO content_clusters (topic_label, keywords, sources, avg_engagement_score, item_ids) SELECT p0::VARCHAR, p1::VARCHAR[],       base.py:1820
                             p2::VARCHAR[], p3::FLOAT, p4::VARCHAR[] FROM (VALUES ($1::VARCHAR, $2::VARCHAR[], $3::VARCHAR[], $4::FLOAT, $5::VARCHAR[] ... 371                  
                             characters truncated ... sen_counter RETURNING content_clusters.id, content_clusters.created_at, content_clusters.id AS id__1                      
2026-09-30 13:44:07,548 INFO sqlalchemy.engine.Engine [generated in 0.00028s (insertmanyvalues) 1/1 (ordered)] ('graphify · filipino · español português', ['graphify', 'filipino', 'español português', 'español', 'entire project', 'entire', 'english 简体中文', 'english'], ['github'], 257328.0, ['gh_1200597263'], 'g4f · gpt4free · litellm', ['g4f', 'gpt4free', 'litellm', 'gateway', 'ai gateway', 'ai', 'openai', 'gpt4free g4f'], ['github'], 139386.0, ['gh_671269505', 'gh_620936652'], 'plugins · code · claude', ['plugins', 'code', 'claude', 'claude code', 'iteration', 'resources', 'agents', 'awesome'], ['github'], 96566.5, ['gh_969302809', 'gh_1100776768'], 'la · ia · el', ['la', 'ia', 'el', 'en', 'openai', 'los', 'que', 'inteligencia artificial'], ['google_news'], 0.5, ['gn_CBMilAFBVV95cUxPM3hkenJKVTdCSE9vRmZPNS03ZDhEZWswaXFPSXd0ZGQ2R0xVX0Z2U1NkQXhEWHFhc19XbmxJV1A3TmlVOEFTLXBCam5wRVpVMDlRWS03NjNyeDlTeElpd0NKNF85bG5FN ... (3867 characters truncated) ... jcGY1VDFTRFBnZXNRcWFIVDliLUgwa2FPVjlxNUY0NTVlY0lsR21qNDgzNV9NYXp4M1VuU0ZEak5mQ0hWU0hZaU1iTHdacFQ1dG1ILWJIcGUwTGRPdDA2X0x2Qnk5Z1RPSUFySHJXV0Z5WmdzUzQ'], 'en · riesgo existencial · que sus', ['en', 'riesgo existencial', 'que sus', 'que', 'para la', 'riesgo', 'modelos ia', 'modelos'], ['google_news'], 0.5, ['gn_CBMilgFBVV95cUxPY19WRnZmTHZ5TUJxSFV4ZTk2bTMtbHJZeGlmZlVyT3dWR0FIVkNkTUp2V1Q1MHdzdU9TUG1DTXVoZVVXMFRqRFpYWHVzNnc2eDNnelNNRkFaWjktWVI5c1VBR2JGcUJNQ1ByOWl5UWQwMTJpalg3dG1XdjV1WTBYc0hsTFFyZnBSa2VGNXh3VnhqM28tVXc'])
                    INFO     [generated in 0.00028s (insertmanyvalues) 1/1 (ordered)] ('graphify · filipino · español português', ['graphify', 'filipino', 'español base.py:1820
                             português', 'español', 'entire project', 'entire', 'english 简体中文', 'english'], ['github'], 257328.0, ['gh_1200597263'], 'g4f ·                 
                             gpt4free · litellm', ['g4f', 'gpt4free', 'litellm', 'gateway', 'ai gateway', 'ai', 'openai', 'gpt4free g4f'], ['github'], 139386.0,                
                             ['gh_671269505', 'gh_620936652'], 'plugins · code · claude', ['plugins', 'code', 'claude', 'claude code', 'iteration', 'resources',                
                             'agents', 'awesome'], ['github'], 96566.5, ['gh_969302809', 'gh_1100776768'], 'la · ia · el', ['la', 'ia', 'el', 'en', 'openai',                   
                             'los', 'que', 'inteligencia artificial'], ['google_news'], 0.5,                                                                                    
                             ['gn_CBMilAFBVV95cUxPM3hkenJKVTdCSE9vRmZPNS03ZDhEZWswaXFPSXd0ZGQ2R0xVX0Z2U1NkQXhEWHFhc19XbmxJV1A3TmlVOEFTLXBCam5wRVpVMDlRWS03NjNyeDlTe             
                             Elpd0NKNF85bG5FN ... (3867 characters truncated) ...                                                                                               
                             jcGY1VDFTRFBnZXNRcWFIVDliLUgwa2FPVjlxNUY0NTVlY0lsR21qNDgzNV9NYXp4M1VuU0ZEak5mQ0hWU0hZaU1iTHdacFQ1dG1ILWJIcGUwTGRPdDA2X0x2Qnk5Z1RPSUFyS             
                             HJXV0Z5WmdzUzQ'], 'en · riesgo existencial · que sus', ['en', 'riesgo existencial', 'que sus', 'que', 'para la', 'riesgo', 'modelos                
                             ia', 'modelos'], ['google_news'], 0.5,                                                                                                             
                             ['gn_CBMilgFBVV95cUxPY19WRnZmTHZ5TUJxSFV4ZTk2bTMtbHJZeGlmZlVyT3dWR0FIVkNkTUp2V1Q1MHdzdU9TUG1DTXVoZVVXMFRqRFpYWHVzNnc2eDNnelNNRkFaWjktW             
                             VI5c1VBR2JGcUJNQ1ByOWl5UWQwMTJpalg3dG1XdjV1WTBYc0hsTFFyZnBSa2VGNXh3VnhqM28tVXc'])                                                                  
2026-09-30 13:44:08,304 INFO sqlalchemy.engine.Engine COMMIT
[09/30/26 13:44:08] INFO     COMMIT                                                                                                                                 base.py:2685
2026-09-30 13:44:08,389 INFO sqlalchemy.engine.Engine BEGIN (implicit)
                    INFO     BEGIN (implicit)                                                                                                                       base.py:2679
2026-09-30 13:44:08,392 INFO sqlalchemy.engine.Engine SELECT content_clusters.id, content_clusters.topic_label, content_clusters.keywords, content_clusters.sources, content_clusters.avg_engagement_score, content_clusters.item_ids, content_clusters.created_at 
FROM content_clusters 
WHERE content_clusters.id = $1::INTEGER
                    INFO     SELECT content_clusters.id, content_clusters.topic_label, content_clusters.keywords, content_clusters.sources,                         base.py:1822
                             content_clusters.avg_engagement_score, content_clusters.item_ids, content_clusters.created_at                                                      
                             FROM content_clusters                                                                                                                              
                             WHERE content_clusters.id = $1::INTEGER                                                                                                            
2026-09-30 13:44:08,394 INFO sqlalchemy.engine.Engine [generated in 0.00197s] (6,)
                    INFO     [generated in 0.00197s] (6,)                                                                                                           base.py:1822
2026-09-30 13:44:08,643 INFO sqlalchemy.engine.Engine SELECT content_clusters.id, content_clusters.topic_label, content_clusters.keywords, content_clusters.sources, content_clusters.avg_engagement_score, content_clusters.item_ids, content_clusters.created_at 
FROM content_clusters 
WHERE content_clusters.id = $1::INTEGER
                    INFO     SELECT content_clusters.id, content_clusters.topic_label, content_clusters.keywords, content_clusters.sources,                         base.py:1822
                             content_clusters.avg_engagement_score, content_clusters.item_ids, content_clusters.created_at                                                      
                             FROM content_clusters                                                                                                                              
                             WHERE content_clusters.id = $1::INTEGER                                                                                                            
2026-09-30 13:44:08,646 INFO sqlalchemy.engine.Engine [cached since 0.2537s ago] (7,)
                    INFO     [cached since 0.2537s ago] (7,)                                                                                                        base.py:1822
2026-09-30 13:44:08,729 INFO sqlalchemy.engine.Engine SELECT content_clusters.id, content_clusters.topic_label, content_clusters.keywords, content_clusters.sources, content_clusters.avg_engagement_score, content_clusters.item_ids, content_clusters.created_at 
FROM content_clusters 
WHERE content_clusters.id = $1::INTEGER
                    INFO     SELECT content_clusters.id, content_clusters.topic_label, content_clusters.keywords, content_clusters.sources,                         base.py:1822
                             content_clusters.avg_engagement_score, content_clusters.item_ids, content_clusters.created_at                                                      
                             FROM content_clusters                                                                                                                              
                             WHERE content_clusters.id = $1::INTEGER                                                                                                            
2026-09-30 13:44:08,732 INFO sqlalchemy.engine.Engine [cached since 0.3401s ago] (8,)
                    INFO     [cached since 0.3401s ago] (8,)                                                                                                        base.py:1822
2026-09-30 13:44:08,817 INFO sqlalchemy.engine.Engine SELECT content_clusters.id, content_clusters.topic_label, content_clusters.keywords, content_clusters.sources, content_clusters.avg_engagement_score, content_clusters.item_ids, content_clusters.created_at 
FROM content_clusters 
WHERE content_clusters.id = $1::INTEGER
                    INFO     SELECT content_clusters.id, content_clusters.topic_label, content_clusters.keywords, content_clusters.sources,                         base.py:1822
                             content_clusters.avg_engagement_score, content_clusters.item_ids, content_clusters.created_at                                                      
                             FROM content_clusters                                                                                                                              
                             WHERE content_clusters.id = $1::INTEGER                                                                                                            
2026-09-30 13:44:08,818 INFO sqlalchemy.engine.Engine [cached since 0.4262s ago] (9,)
                    INFO     [cached since 0.4262s ago] (9,)                                                                                                        base.py:1822
2026-09-30 13:44:08,904 INFO sqlalchemy.engine.Engine SELECT content_clusters.id, content_clusters.topic_label, content_clusters.keywords, content_clusters.sources, content_clusters.avg_engagement_score, content_clusters.item_ids, content_clusters.created_at 
FROM content_clusters 
WHERE content_clusters.id = $1::INTEGER
                    INFO     SELECT content_clusters.id, content_clusters.topic_label, content_clusters.keywords, content_clusters.sources,                         base.py:1822
                             content_clusters.avg_engagement_score, content_clusters.item_ids, content_clusters.created_at                                                      
                             FROM content_clusters                                                                                                                              
                             WHERE content_clusters.id = $1::INTEGER                                                                                                            
2026-09-30 13:44:08,906 INFO sqlalchemy.engine.Engine [cached since 0.5137s ago] (10,)
                    INFO     [cached since 0.5137s ago] (10,)                                                                                                       base.py:1822
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
[09/30/26 13:44:09] INFO     AFC is enabled with max remote calls: 10.                                                                                            models.py:6224
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
                    INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
INFO:     127.0.0.1:51084 - "POST /mcp/ HTTP/1.1" 200 OK
[09/30/26 13:44:10] INFO     HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 404 Not       _client.py:1025
                             Found"                                                                                                                                             
Campaign generation error (cluster=graphify · filipino · español português): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Campaign generation error (cluster=g4f · gpt4free · litellm): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Campaign generation error (cluster=plugins · code · claude): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Campaign generation error (cluster=la · ia · el): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
Campaign generation error (cluster=en · riesgo existencial · que sus): 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.0-flash is no longer available. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
2026-09-30 13:44:10,256 INFO sqlalchemy.engine.Engine ROLLBACK
                    INFO     ROLLBACK                                                                                                                               base.py:2682
2026-09-30 13:44:10,338 INFO sqlalchemy.engine.Engine ROLLBACK
                    INFO     ROLLBACK                                                                                                                               base.py:2682
2026-09-30 13:44:10,420 INFO sqlalchemy.engine.Engine ROLLBACK
                    INFO     ROLLBACK                                                                                                                               base.py:2682
2026-09-30 13:44:10,499 INFO sqlalchemy.engine.Engine ROLLBACK
                    INFO     ROLLBACK                                                                                                                               base.py:2682
                    ERROR    Tool 'run_marketing_pipeline' raised an unexpected exception                                                                          server.py:446
                             ╭──────────────────────────────────────────────── Traceback (most recent call last) ────────────────────────────────────────────────╮              
                             │ /home/aleosh/Documentos/Jobs/Neurotry/newsss-core/venv/lib/python3.14/site-packages/mcp/server/mcpserver/tools/base.py:176 in run │              
                             │                                                                                                                                   │              
                             │   173 │   │   │   │   │   return self.fn_metadata.convert_result(resolved) if convert_result                                      │              
                             │       else resolved                                                                                                               │              
                             │   174 │   │   │   │   pass_directly |= resolved                                                                                   │              
                             │   175 │   │   │                                                                                                                   │              
                             │ ❱ 176 │   │   │   result = await self.fn_metadata.call_fn(self.fn, self.is_async, validated,                                      │              
                             │       pass_directly)                                                                                                              │              
                             │   177 │   │   │                                                                                                                   │              
                             │   178 │   │   │   # Registration rejects the annotated form of this combination; this covers                                      │              
                             │   179 │   │   │   # a body that returns an InputRequiredResult without declaring it. It is                                        │              
                             │                                                                                                                                   │              
                             │ /home/aleosh/Documentos/Jobs/Neurotry/newsss-core/venv/lib/python3.14/site-packages/mcp/server/mcpserver/utilities/func_metadata. │              
                             │ py:163 in call_fn                                                                                                                 │              
                             │                                                                                                                                   │              
                             │   160 │   │   """                                                                                                                 │              
                             │   161 │   │   kwargs = arguments | (arguments_to_pass_directly or {})                                                             │              
                             │   162 │   │   if fn_is_async:                                                                                                     │              
                             │ ❱ 163 │   │   │   return await fn(**kwargs)                                                                                       │              
                             │   164 │   │   return await anyio.to_thread.run_sync(functools.partial(fn, **kwargs))                                              │              
                             │   165 │                                                                                                                           │              
                             │   166 │   @deprecated(                                                                                                            │              
                             │                                                                                                                                   │              
                             │ /home/aleosh/Documentos/Jobs/Neurotry/newsss-core/src/features/marketing/presentation/mcp_tools/run_pipeline.py:66 in             │              
                             │ run_marketing_pipeline                                                                                                            │              
                             │                                                                                                                                   │              
                             │   63 │   │   │   campaign_type=campaign_type,                                                                                     │              
                             │   64 │   │   │   translate_non_english=translate_non_english,                                                                     │              
                             │   65 │   │   )                                                                                                                    │              
                             │ ❱ 66 │   │   result = await use_case.execute(config)                                                                              │              
                             │   67 │                                                                                                                            │              
                             │   68 │   campaigns_data = [                                                                                                       │              
                             │   69 │   │   {                                                                                                                    │              
                             │                                                                                                                                   │              
                             │ /home/aleosh/Documentos/Jobs/Neurotry/newsss-core/src/features/marketing/domain/usecases/run_marketing_pipeline.py:165 in execute │              
                             │                                                                                                                                   │              
                             │   162 │   │                                                                                                                       │              
                             │   163 │   │   # Mark source items as processed so they aren't reused in future runs                                               │              
                             │   164 │   │   yt_ids = [item.raw_id for item in items if item.source == "youtube"]                                                │              
                             │ ❱ 165 │   │   gh_ids = [int(item.raw_id) for item in items if item.source == "github"] #                                          │              
                             │       GitHub uses int                                                                                                             │              
                             │   166 │   │   gn_ids = [item.raw_id for item in items if item.source == "google_news"]                                            │              
                             │   167 │   │                                                                                                                       │              
                             │   168 │   │   if yt_ids:                                                                                                          │              
                             ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯              
                             AttributeError: 'NormalizedItem' object has no attribute 'raw_id'                                                                                  
                                                                                                                                                                                
                             The above exception was the direct cause of the following exception:                                                                               
                                                                                                                                                                                
                             ╭──────────────────────────────────────────────── Traceback (most recent call last) ────────────────────────────────────────────────╮              
                             │ /home/aleosh/Documentos/Jobs/Neurotry/newsss-core/venv/lib/python3.14/site-packages/mcp/server/mcpserver/server.py:433 in         │              
                             │ _handle_call_tool                                                                                                                 │              
                             │                                                                                                                                   │              
                             │    430 │   ) -> CallToolResult | InputRequiredResult:                                                                             │              
                             │    431 │   │   context = Context(request_context=ctx, mcp_server=self, input_params=params,                                       │              
                             │        subscriptions=self._subscriptions)                                                                                         │              
                             │    432 │   │   try:                                                                                                               │              
                             │ ❱  433 │   │   │   return await self.call_tool(params.name, params.arguments or {}, context)                                      │              
                             │    434 │   │   except MCPError:                                                                                                   │              
                             │    435 │   │   │   raise                                                                                                          │              
                             │    436 │   │   except Exception as exc:                                                                                           │              
                             │                                                                                                                                   │              
                             │ /home/aleosh/Documentos/Jobs/Neurotry/newsss-core/venv/lib/python3.14/site-packages/mcp/server/mcpserver/server.py:539 in         │              
                             │ call_tool                                                                                                                         │              
                             │                                                                                                                                   │              
                             │    536 │   │   """                                                                                                                │              
                             │    537 │   │   if context is None:                                                                                                │              
                             │    538 │   │   │   context = Context(mcp_server=self, subscriptions=self._subscriptions)                                          │              
                             │ ❱  539 │   │   return await self._tool_manager.call_tool(name, arguments, context,                                                │              
                             │        convert_result=True)                                                                                                       │              
                             │    540 │                                                                                                                          │              
                             │    541 │   async def list_resources(self) -> list[MCPResource]:                                                                   │              
                             │    542 │   │   """List all available resources."""                                                                                │              
                             │                                                                                                                                   │              
                             │ /home/aleosh/Documentos/Jobs/Neurotry/newsss-core/venv/lib/python3.14/site-packages/mcp/server/mcpserver/tools/tool_manager.py:87 │              
                             │ in call_tool                                                                                                                      │              
                             │                                                                                                                                   │              
                             │   84 │   │   if not tool:                                                                                                         │              
                             │   85 │   │   │   raise ToolError(f"Unknown tool: {name}")                                                                         │              
                             │   86 │   │                                                                                                                        │              
                             │ ❱ 87 │   │   return await tool.run(arguments, context, convert_result=convert_result)                                             │              
                             │   88                                                                                                                              │              
                             │                                                                                                                                   │              
                             │ /home/aleosh/Documentos/Jobs/Neurotry/newsss-core/venv/lib/python3.14/site-packages/mcp/server/mcpserver/tools/base.py:210 in run │              
                             │                                                                                                                                   │              
                             │   207 │   │   │   raise ToolError(f"Error executing tool {self.name}: {exc}") from exc                                            │              
                             │   208 │   │   except Exception as exc:                                                                                            │              
                             │   209 │   │   │   # A crash: the exception's own text stays on the server.                                                        │              
                             │ ❱ 210 │   │   │   raise UnexpectedToolError(f"Error executing tool {self.name}") from exc                                         │              
                             │   211                                                                                                                             │              
                             ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯              
                             UnexpectedToolError: Error executing tool run_marketing_pipeline                                                                                   
