require 'sinatra'
require 'sinatra/cookies'
require 'sanitize'
require 'open-uri'

require_relative 'config.rb'
require_relative 'gen_svg.rb'
runes = [
    "ᛆ", "ᛒ", "ᛍ", "ᛑ", "ᛂ", "ᚠ", "ᚵ", "ᚼ", "ᛁ", "ᛂ", "ᚴ", "ᛚ", "ᛘ", "ᚿ", "ᚮ", "ᛕ", "ᛩ", "ᚱ", "ᛋ", "ᛐ", "ᚢ",
    "ᚡ", "ᚢ", "ᚥ", "ᛪ", "ᛦ", "ᛎ", "ᚭ", "ᛅ", "ᚯ"]
latin = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
    "v", "u", "w", "x", "y", "z", "å", "ä", "ö"]
Rmap = Hash[latin.zip(runes)]

set :templates, Dir.glob("templates/prod-??.svg").map{|f| File.open(f).read}

before /\/(logo|dev)/ do
  if(cookies[:user])
    begin
      @user = Crypto.decrypt(cookies[:user]).encode("UTF-8", invalid: :replace)
    rescue Exception => e
      halt 501, 'oh no cookie problem!'
    end
  else
    @user = nil
  end
  @str = params["str"]
  @str ||= @user
  @str = Sanitize.clean(@str).encode("UTF-8", invalid: :replace).downcase.split("").map{|c| Rmap[c]}.join("")[0..6]
end

get '/' do
  generate_front()
end

post '/setstring' do
  str = Sanitize.clean(params["str"].encode("UTF-8", invalid: :replace))
  if (str.to_s.size > 0 && !(/\Aadmin\z/).match(str))
    cookies[:user] = Crypto.encrypt(str) 
    redirect "/logo"
  else
    redirect "/"
  end
end

get '/logo' do
  redirect '/' unless @str
  generate_svg(@str, settings.templates.sample)
end

get '/dev' do
  halt(401, 'unauthorized') unless /^admin$/.match?(@user)
  halt(400, 'missing parameters, try /dev?str=foobar&template=templates/dev-01.svg') \
    unless(@str && params["template"])
  begin
    tmpl = open(Sanitize.clean(params["template"])).read
  rescue
    halt 500, 'could not read template'
  end
  generate_svg(@str, tmpl)
end

after '/dev' do
  # prevent data leaks
  response.body[0].gsub!(/[A-Za-z0-9+\/=]{25,}/,"") if response.body[0]
end

