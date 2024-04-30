require 'openssl'

module Crypto
  @iv = [ENV["LOGOIV"]].pack("H*")
  STDERR.puts @iv.length
  @iv = OpenSSL::Random.random_bytes(16) unless @iv.length == 16
  @key = [ENV["LOGOKEY"]].pack("H*")
  @key = OpenSSL::Random.random_bytes(32) unless @key.length == 32

  def Crypto.encrypt(str)
    aes = OpenSSL::Cipher::Cipher.new("AES-256-CBC")
    aes.encrypt
    aes.key = @key
    aes.iv = @iv
    cipher = aes.update(str)
    cipher << aes.final
    return([cipher].pack('m'))
  end

  def Crypto.decrypt(data)
    dec_cipher = OpenSSL::Cipher::Cipher.new("AES-256-CBC")
    dec_cipher.decrypt
    dec_cipher.key = @key
    dec_cipher.iv = @iv
    plain = dec_cipher.update(data.unpack('m')[0])
    plain << dec_cipher.final
    plain.force_encoding("utf-8")
    return(plain)
  end
end

