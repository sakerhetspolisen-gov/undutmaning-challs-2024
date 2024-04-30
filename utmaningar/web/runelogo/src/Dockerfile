FROM ruby:2.7-alpine
WORKDIR /srv
COPY . /srv
RUN gem install bundler:2.3.22
RUN mkdir -p /usr/include/sys
RUN echo "#include <unistd.h>" > /usr/include/sys/unistd.h
RUN apk add g++ && apk add make && apk add openssl
RUN bundle install
EXPOSE 4567
CMD ./start
