# Nginx 配置反向代理
这里给出了在CentOS环境下如何配置nginx反向代理,避免直接使用ip:port模式访问方法.

## Nginx的下载与编译安装
* ***APP_PATH***表示nginx的安装位置.
* ***DOWNLOAD_PATH***表示下载位置.
* ***LOG_PATH***表示日志输出位置.

以上变量在下文中注意自行替换.

```bash
# 安装一些前置依赖
sudo yum -y install gcc openssl-devel pcre2.x86_64 pcre2-devel.x86_64 zlib.x86_64 zlib-devel.x86_64 

# 开启80端口访问
sudo firewall-cmd --zone=public --add-port=80/tcp --permanent 
sudo firewall-cmd --reload 

# download and unpack
cd $DOWNLOAD_PATH
wget https://nginx.org/download/nginx-1.24.0.tar.gz
tar zxvf nginx-1.24.0.tar.gz
cd nginx-1.24.0

mkdir -p $APP_PATH/nginx1.24.0/runtime
./configure --prefix=$APP_PATH/nginx1.24.0 \
--pid-path=$APP_PATH/nginx1.24.0/runtime/nginx.pid \
--with-http_ssl_module --with-stream

make
make install
```
## Nginx配置
```bash
# 安装完毕进入安装目录进行配置
cd $APP_PATH/nginx1.24.0 
mkdir /conf/vhost 

vim conf/nginx.conf 
```

在此文件中输入如下内容(**注意修改USERNAME为当前用户名**):
```
user  USERNAME USERNAME;
worker_processes  4; 

 
error_log  $LOG_PATH/nginx/error.log; 
pid        $APP_PATH/nginx1.24.0/runtime/nginx.pid; 

events {
    worker_connections  65535; 
} 

http {
    include       mime.types; 
    default_type  application/octet-stream; 

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" ' 
                      '$status $body_bytes_sent "$http_referer" ' 
                      '"$http_user_agent" "$http_x_forwarded_for"'; 

    access_log  $LOG_PATH/nginx/access.log  main;
    sendfile        on; 
    #tcp_nopush     on;

    keepalive_timeout  65; 
    client_max_body_size  256m; 

    fastcgi_connect_timeout       300; 
    fastcgi_send_timeout          300; 
    fastcgi_read_timeout          300; 
    fastcgi_buffer_size           64k; 
    fastcgi_buffers             4 64k; 
    fastcgi_busy_buffers_size    128k; 
    fastcgi_temp_file_write_size 256k; 

    gzip on;
    gzip_vary on;
    gzip_min_length     1k;
    gzip_buffers     4 16k;
    gzip_http_version  1.0;
    gzip_comp_level      5;
    gzip_types  text/plain application/x-javascript text/css application/xml; 

    include $APP_PATH/conf/vhost/*.conf; 
}

```

保存文件并退出,然后

```bash
vim conf/vhost/lawyer_llama13B.conf
```

在此文件中输入如下内容:
```
upstream lawyerllama_backend {
    hash $remote_addr consistent;
    server 127.0.0.1:7863;
}

    server {
        listen       80;
        server_name  lawyerllama.localdomain.com;

        access_log  $LOG_PATH/nginx/lawyerllama.access.log main;
        error_log   $LOG_PATH/nginx/lawyerllama.error.log;

        location / {
            proxy_pass http://lawyerllama_backend;
            
            proxy_http_version 1.1;
            proxy_connect_timeout 5s;
            proxy_read_timeout 60s;
            proxy_send_timeout 30s;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "$connection_upgrade";
            # proxy_set_header Connection "Upgrade";
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
```
保存文件并退出.
## 运行
修改***demo_web.py***的最后一行,将参数***share***修改为***True***, ***server_name***修改为***127.0.0.1***.
启动法条[检索服务](./run_inference.md)和[交互界面]((./run_inference.md)).

```bash
cd $APP_PATH/nginx1.24.0 
sudo ./sbin/nginx  # 启动nginx server
sudo ./sbin/nginx -s stop  # 停止nginx server
sudo ./sbin/nginx -s reload  # 重载nginx server
```

## 访问
在客户机电脑上绑定***lawyerllama.localdomain.com***到服务器ip,然后通过浏览器访问此域名即可.