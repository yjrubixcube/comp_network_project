import cv2, numpy as np, base64

s = b'TrGxKD8DU9uo5PHNLdMBFtB5PpQBUi81IgfKJpJHkaZA0RGOavQrhBnORTfvXPBPA9KWxREZcDmN/wAqrw3A3yMUkGf9k1oOSoPPb0qCAfITkcmpKRTu7pBA/wB7OMciubkbrjqa6fV22Wb/AHcn2rmZPbFQy0iMYyPrWpHcQxlFZxnHrWWgzIBWxDFF5gLxqSB1IqL2KSOW8bQRXMSHIx0znpXl91C0M7I3BFd34r1lb3VZLKxRTHEhZ2XpxXH3jrcpz/rE/UV5mIactD06KtHUztvPNJIoxipQQcimvjHvXMtGbXM6aBTTra3j7k1YePOadDZM5BB4qk7s1UtC9YWkDEHGTW7axJGAB0rKsbKSPHNasasODXTCViJSItWtkngJC/MOhqnpduyHLZ4rVcZUKafFEFAUUnG8rmUpaFi0Xcc961o/lC+pqhAoXHarkbAyIM98VrGJg9Tj/iRB9n1aC4XgSR4P1Fcva6pLaXKywuVYHOQa7n4rJ/oFk+BwzDP4V5cx963nocE9z27wh4wTU4ltp32zAevWu+hmBRdp7V8tWV7JbTK8blWU5BFd3pXxBubZY0ugJFHGRwacKtlqQlc9omkYyqM/pVgTH/IrgdL8aWF86kzbH/uvXTQapBIAyuWB/u81oqiewOLF1qTdOufSs0Gl1G6SW4ypOMdxiqwcEcGtLisX7fBbnBr4x1f/AJC17/13f/0I19k2rEc5r421f/kK3v8A13f/ANCNYV+gJFSiiiuYYUUUUAFFFFABRRRQAUUUUAFFFFAF3RP+QzYf9fEf/oQr76EKgcO4z718C6LxrFh/13j/APQhX36s0JjH7wdK68KtzOZjayrLtXexB9ayMcmr+pzGSfBYFV6VSFdbJRb0yLzLhRnGK6NIpAhxJ+aisnRYx5m49cVuPkx8AgUgGRxzhQFMZ9cimzxSh41byzmrsQ2gDBqGQh7of7IptjsKqShfuA/8CxVeLzDI7GI+n3qusQFPsKr22PLz6moKRDO7LG5Mb9PrTI5QkSgxy/8AfNT3jHy8A9TinhsKB6D1obKRh63cK8SIA4PuMVhOwPFbevyjzEX0FYM0qRqS7BR7mspPuaJEtoAZ1yQADnmsPxl4kFoktrYyZkYYd1/hHpWdrXiMRK0Ng4Lngv6fSuKvJHkZEGWlmYKPcmuOrXS0R1U6XVm1oUZh0m5v5f8AWXTbEz/dFYN2TFOcdQa6nxBts7WC2jxtgjC/jXL3jLLEko/iFede71PQivdIBICSw707cCMmqe8oeOlSCRSOeKb3FsSM2DVyzmG33FZkjDtSJMVOc01KxaaOzs5QygGrLEEcda53T75dqjOT71qpcgjJIxW8ZGU2W0UE81OoA6VTScMcLz+FWY8nGetaKxCi2y4nX2qbS/8ASLwsv+rQ7R7nvWVeXJ+WCHmV+PpXSaNbLBAqgdBW1Jc0rGddqETn/ikoOi25J5EnH5GvJJDg16x8UpCul2yMBzJn9K8mmIOa0r6M82TIi2DTZHOODSNjPFMfpxXI2ImjunXAB5+tbmn61d2oBinkUj0auW3HOfSrKSnb15rLmZpGXc7+18b3seFldZMf3gDWza+NoHwJ7YD3Q4ryUyENk1PFOQck1pGq11BtHtdn4m06YYErR57MK+WtTIbUrsjkGVyPzNekRXoxgGvM7k5uZT/tn+dac7luQ1YiooooEFFFFABRRRQAUUUUAFFFFABRRRQBd0X/AJDNhnp9oj/9CFfeRazIO6N1/Aivg3RP+Q1Yf9fEf/oQr72u5QsDng114Z6MiZzs7RmVjGCFzxUYwT3pHbJJpFPzCupslG1ptossWTK6E+hq/wDYCpULdS4+tVrGGJoELLk+uatCBPMwC4GPWkmA/wCw3Wf3d8fxqBIL/eWFwpbpyKseTtBxNIPxqGJJGGVuCPqBQ2NBK2oxIcmNxTEnv1Rf9HQj60y8eeKEl512/wC1xXNat42tdNzHHIlxIOMJnH51lKajuzSMXJ6HQXF7chlWS2GevBrJ1LxnZWG5ZUzIP4VavOdf8a6hqBYCTyIugVOP1ri7m8aRjucknvXHUxa+wdUKH8x3mu+Ori9nJtIliB4BJya5i71K4uX/AH9wzdyM1z73giXcTwKbDceYCSeTzXJKrKW7N0ox2NkyjtnNXPCMIvvEsbMMpbKZD9e1YccmFyTXTfDcfu9Tuj1JC/hUblXLnixt1rPL3AJrktNmE2kRA/eBINW/GOt3kmqzWytGkCYXaiDnjv61R047owFkKZ64QAVUoXeg/bqGjGXKHGRmqoYg9TW9HZNIDm4OMf3Aas6XpEF3dxwyyEFmC/cFP2EmP6zA5kyOO+aj852fAXNdj4t0O00+G2e0RxuQF2JzknpXNQeWkm5u1ZzpOm7M2hJSV0SW0cu4E8VrQDIAYms/7QpORVi3n5yelOLS0K5bm3bZA44qa6vFtojzlz0FY7X4RcKcmp9IspL+4Esv3Ac8960i7uyCVoK7Nvw5aSTSm4nyXbpnsK7SBAqACqOnwLHGoAxgVfBZei5r06NPlR5FerzyOA+LJb7PZnJxub+VeWyGvUPiy/8AolmpGCWY4/CvK3PPrWOIfvWMXsMJ5qInBp7Gomrie4EZPrShiOhqNzhj1pu45NZ9QJvMzS7sHFQBu2aUmi4XLKy4FcZN/rn/AN411YNcpL/rX+prak9wvcZRRRWoBRRRQAUUUUAFFFFABRRRQAUUUUAXdF/5DNh/18R/+hCvurVti23Gck18K6L/AMhmw/6+I/8A0IV9x6wcKimuvC9SJGSw4pYV3SACkNT2a5nWup6CRtQQMgUeYwGO1PjWXc+JmyOORmpWbEZIxwK5fVfFNppKOpfzZ88Ip/nWbkoK7KUW3odJcyyRQO7zIAOpYYrj9X8cQ2CGK02TyAfe/hFcP4h8U32qsfNkKQ54jU4FcxdXXBOea4quKe0Trhh0tZHQaz4jvdRcm5nYr2UHAFc1dXo5weazbq92j7xrJmu2YnBxXDKTbuzdtRWhpz3xz96qDXLO2F5rOklY96VWKQlifmPAqTN1Cee4JcKDlVq5YSbsk9KxN1X7CQ/dHrRciM7s2biUpbO35V2nw3bPh26bu0nP5V53qkoW3C55Ndp8NLkPpN1DnlXzj8KFujW/vDtQRLaabZZwiSVsiWcHGPUVhLbRB5DbxsZQ3zSSZCfhWprxVrpVEbXTqeUfACn2rOMyOdpP2tg/EAACp+tbkzWpTWJInY24leYHq7kIPpW/4WS2uGmtZYpWLPuaYysuwdPlNZsoWYFWPnENxbx8BfxrU0GNftTJIhkGRiFf4fcnNVC/MZlVAfsuoqbieUR3AjTzHz8ozis8qe9bs9vttL1xjBkQ8fjWO54xiprnfhdUyNfSpVJHGajA71d0+1e5lCjp3Nc0VqdDaSuyxptm93MBg7B1Nd9plmsaIqKAAKz9LsVhRVUYx1966S0jwg7V6WHo21Z5uIr8+i2LEY2KBipTIoAGDn6UwHkUkkiqpJ4A5Nd2xwvVnl3xavRJqNtbL1jTcfqf/wBVedO3NbPizUDqGt3dxnKlyF+g4FYOcnmvNrSvIp9hxw34UyQ8cU8fKKgkcc1hIkjl7EUzNLnKkVHnnmsgH5pOc0wMSacDSAfniuXk/wBY/wBTXTZ4rmZP9Y31Nb0QQ2iiithhRRRQAUUUUAFFFFABRRRQAUUUUAXdF/5DFh/13j/9CFfburY+0/LXxFo3GsWJ/wCm8f8A6EK+1ruUSXDMORXZhepEiE9KzdR1y30n7x3zn7sYP86n1S8Wzs5ZmOAgJrx+91N7iea5mclnPHsPSjE1XTWm5tRp8z1Ov1bxnfXUbx+YIUPUJ/jXH3d/ySzbmPesq4vc9yazrm6yeDivNlUlL4mdnuw2NKe+xnmsy5vG5OapzXGeKqu5Y8moIlUJprgvjJquzZ701jTSSBUmMpNjlALdaR33MeeBwKYSQOKaDk80CuKau6cwEwyaonk1LbvtcGgS3J9Tl3zYHQV0nw5vPIvpo2PDr0964+V98hI6Vu+Ecrfow67sU1uW5e9c6vxNITcK1yZFTdhGTqax3YqB9obykLZHlcs31rQ1p5RdghkhJ5yed3uOazIeDmD9wxbl5e/0rRvU1mWFcoo87EURfhoz8zfWt/Rdu/LP5cZ/iX7z+xrBt12MXtwY23fM8ucH6VtaBLI1w7QoFfozPnBHtV09GZly4ATR7xR1MqH9DXOMa6C+JTR592CTOv8AKsmys5LtwAuF7mlWV2jvwzUYNsjs7WS5lAQcdzXY6TYpboqjk9zTLK0jt41WMYrVtoxkGrpUrMwr1ubRF62j6YrVjXCCqVqhAq4pOK9CGxwy1HrwawPG+pDTtAuZAcSOPLT6n/61bpNeT/FfVvOvo7CNvlhGX/3jTqOyuSjgJZMsTnqaYCOvemE80ua8pu7uxMc7VWkPNSueKrscmpnsAmeaY/BpSaU8rWQDB1pwpq08CgQvauZk/wBY31NdRjiuXk/1jfU1vSGhtFFFajCiiigAooooAKKKKACiiigAooooAt6R/wAhay/67p/6EK+14+lFFdmF2ZMjnPHn/IBn+lePTf6miiscZujqw+xlzdTVObv9KKK89lyKzfeppoooMmNamN2oopEjDSL94UUUAOPWk9aKKEIj710HhD/j9H++KKKa+Ia3NPxF/wAflpUGs/ct/wDeooq3udE+hpXn/IPj+taNl/x72v8AvUUVpHdGRpaj/wAgL/tv/wCyipdF/wBQtFFOXxI6ofwzbSr9t1WiiuiG5zTNW2+7VgdqKK6oGApr5/8AHn/I0X//AF1NFFZ1/hBdTnO9L3FFFecyRrdKrN96iiokIYehpw6H6UUVn1Gxq9TTx2oopiFP3TXMSffb60UVtTGhtFFFajCiiigAooooA//Z'
t = b'/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCADhAZADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5UooooAKKKKACiiigC3pP/IVs/wDrsn/oQr7KDS44Jx9a+NdJ/wCQrZf9dk/9CFfZhHyda78FsxMmsjcHLIRnpyatFrsyqp2fnTrJAIhmnwLm4ZienGa6rEpkhkuwhPyfmakgN3hceXjryTTpDhAM8k1KCFX72MCjbQaZjahLMZiJGHHoapl2/vGp7t90znORmoBjNS+w7l3TpGVifmJ9qtXErsFDLIMmoLJ4o4smQBs1akuIWkjxKu1ev1qBjmnZQBsl4qtDcPvkbEuCana6g5/fLmmJPCI8GVc5zUvQtGP4nvpYtNfZ5oJ74rzbUrSS3R5xcMFk6qDnP1r1a+lglIV3RkArzvxOkccjLGpK9R6V5WYKXKmj0MJJaqxyl3cvFF8rke9YF5ctMG8w7s+ta17IJIDuGAK5q6kRHIBJFeKk7nbOehlXcbI5IOAe1V3ZmHoa0pisi9DVVgin5hxXRGbscU4q90UsE/WrEX3Rng+tSFYjhkbHsaR2yMYyKtyuSkTRTMx255HepEjKvnofasws0bblOatW2ogMPNTI9qlxfQtSWxrwQee2MgP796imtZI38yEnzE5K96l+0xGMNH07NVWa7d2DBiGHQ5pbFuwlzdQ3UWSPLnXv2P1q1puslLdoLgZHZh1FYd25dy2ArHrjvUcJ65q+hPMdCupsxwSTjgGrlhMzlgST3rmrcnzK6LTQRGWHWs3e9jRM1UlLZyfmHc9xU0cmVww4NZP2vEhDDj1p0cpyRu47VS0E3c2I4g5O0nJr0LwTHLbaUVnJBzkV5xpxJmXBr1rRRjTYwcdK7ML70jCq7IuRzYz83U1I064+ZxUSAEY2gmhowDkqpr1kcjLSShv+WmBiq1+w2KA5PNXIQpTPlp+NUtSVVCYUD6VexJQc4BOea+StU/5Cd3/12f8A9CNfWbng18map/yErv8A67P/AOhGufEdCZFWiiiuYkKKKKACiiigAooooAKKKKACiiigC3pH/IWsv+u6f+hCvtRoslVHrXxZo/8AyFrL/run/oQr7dix5y56V3YN6MmRYS1Ty8tnOPWmw20W0k5yT61akkjEJ55+lNjeMIvzc9+K7HqQQPDF5qgA8e5p0saLAzAHOPWkadDMxDE4GOlR3U6Lbn5sk1L0GjKYZJ96THFBYUgYEVNy0wI4pCBRmlxnpUPUZGRTGU1KRTXHHFSykyrLgKc9K5jxGWKqhJC4rqZ1JRh6iuQ8VvKsSngJ2I615eYyahY9HBK7ZyN7ZyxhiTuQ965i6iy7etdFPcPOpQkg1h3ETKxzzz2ryIbnVUtYoFNoqvMmVNaJhLDnimG3JGMVoc7VzJSM9xQU2nPP0rQa2K9qikhZe3FURyMz5F5I7VAIsNmtJoT1xTRb5PpTUrC5Rlm7J8o6HqDUkw544qWGDaelSPCzH7tQ3qaJFCZOOOtMhifHStmKwdwBsq/b6Q5I+U1auw5DGsrZi+SDXRWkYWPB71r6ZofTcuK1n0RRGSuOnarjSbd2WtDip4SH5qIqysDn8a29TszFwBjFZSIXYKevaicbE21NHSmIkU9ga9S06UtpMTK3fHFebabasMEV6JpCf8StFHZq1wb/AHljGt8JOJXXoxpRLKT980mzmlCGvZORkyXEq9JDSyTO4HmMTUJU0u096oi9xWBKmvkzU/8AkJXf/XV/5mvrQr8pFfJmp/8AISu/+uz/AMzXPX6ElWiiiucAooooAKKKKACiiigAooooAKKKKALmj/8AIXsv+u6f+hCvuiwTdKzEcCvhfR/+QvZf9d0/9CFfdlnHcCMmMoAfUV1Yd2uTIs3CgwqoGMmlYKDgDoKjK3jyqu6LPbinPDerGx3Q9K7YSIILdAN7YySfSqWtthAuB+VXI4r0RrtMPrzWTqZmMuJSpYf3apoZQJqxZBTJ8wyKr7TVmyBLkE4FQ0Ui3O8WxlAAz3xUFxLb7Asa/MO9NvXQLsTBPc1UUcVAxc0hp3GKYaTuUiQBDbuSMtXnHi+7IRwSR2CEV3zsVBxXnvj8MwTb0PJry8wjdI9HBytc4l5mkbP3fenRDzGxnNQN1wBWnp0QA3Y615qia8zbES0LHJHFT/Y07irgHFDdK15UaJGe1lG3GMUx9OjYc1eyCacBmk0jT2aMWbSiB8vIqqNPcHGK6gKcdKBCCQSADQoXJdNGNaaWX4IP5Vr2mjqD8y1p2sYUdKtlgoBFaxppIlQZXttLiAAKjiti20+HAwoz9KqwS5Nads4BFb04q5TjZD1tkQcDmkKcdKsZyKaehrZxSJRzGvWnyMQK5cwqsnzcHPBruNYAMOa5S4UM5UjrXLViRM1rCIFFZevQ12Om82CAdm54rj9Bjd12jJx1FdpZx+VaDIwzGssLH94c1V+6WooPMPFSvZOgzwRTYJDH0FXPPEkWBnJ7V7ljiZU+wycHjmopoHiOHFXzKyKA+RVG5lMsh5JA6U0RciPIr5I1T/kJ3f8A12f/ANCNfXGPl4r5H1T/AJCd3/12f/0I1hiOgIq0UUVzDCiiigAooooAKKKKACiiigAooooAuaN/yF7H/run/oQr74t0/dIO1fBGi/8AIZsP+viP/wBCFffgi+Xh2GB2Nb0epEhYsGUn06UtxzFjP3jTIICYyxeTJPrRJAxdAJH+ma6oskGAVcegrmb9t9w5966K7ikWFyJGArmZMknPrXRF3QEBGDTWdgCFOM1KRUTg0mWiPk804UCpoImlbCioAYqM3Sn3cDQqp7GrtuY4QVlGGqZ4vtKgMCE7VMkWmc9Jk5FcV41izAMkj2xXdXMflyOvPBrmvE0Cvb7mP3T+dcGLhzQOzDTtI8okGJOa1LHPl1SuUP2lvrWjaIVjFeWkdC+IsjpzSMcDjpQDxzTW9Kts6IkWeaeppu2lHbpUGqZbj6UuMGltgD1qyIh6c1ohXEhkY9aslsrVdVAPFWETI4rSIBGTu4rTtpDtGaoRRkGr8KcVqrg9i5HLuFSZJyR0qqoxipw3y4q077mZQ1PBtyc1y867Zxmur1Bd1u4A7VycpMl0q+lYVNGZ1NjpfD9sxmEiZ54I9RXVsNrKrDoKpeFbPbaq2Ov3c1uXluCg/vjp71rhaV5c6OCrK+hQzU9rMFyCOvtVVuDhhg01Wwc16VzmZsSKjqAwzWdIgWRgOBUsVyw4PIpHIdycdaaIZFjivkPVP+Qnef8AXZ//AEI19gFfl6V8f6r/AMhO8/67P/6Ea58R0GirRRRXMMKKKKACiiigAooooAKKKKACiiigC7on/IasP+viP/0IV9/mRRH99eeOtfAGif8AIasP+viP/wBCFff0jIyKvkkc1rSe5EyWNlWNV3jPfmmhkaVm3/dHrR5kQOWhbj2qGOSEKxMRO48cV0xZBHqkqi1IV8sfeuccVs6pJCwVUiKn1NZbY9K2jIZVIOfamOMirRAx0pqxbmAFVe5RVVTuA962YY/ItyVwSeKqxWqmX5pFAHrVyeK3SLcJBuHo1DGOEA2AMASevNRwsys6HGE/lT2nj2LtkBYjpmovs0bIzPJlm6/NWTKRg38264kYkYBrmNW1OyZWgeZd7DK8cZrY8VQPa2N00DAkRkg+leWlmki3zHLhuCa8/FVHHRdT1sDhHVg6vYjuokY7x13c1ZUYUfSmMu6JSO7ZNTuNqVwQ8y5R5WRcZppIFV5JWBO0dKpS3EpboabGpGpu+lBI4zWM126ckVLDqCn74xSZSmjdtpMNgVeQ561gw3aE8Gr8FyMjmnGVkXzXLEkhWXFW4JQQKzriRSytRFcohHOKtSGb0Z54q9EMj0zWFBfRdCwq6moxr3FbxYnI1AppRkcVUhv4XP3qvRMjgEEVW5DkhrJvUqec1yotcasU5BDV3CRArwK5i5hYanIVHJIrOok1Yxm7qyO8sbcrHGkTbSq1ct4wzN5rkuPeuY07Wktb+K2kfLtgYJ9a6iSQecCBk9+K7qDio8qOKvSlT1l1KWpW67PMXOe9Z6jFauoXIMITyyM+tZyEelbWOe49F7VPGtRx8npVpBVJEMNvFfG+rf8AIUvP+uz/APoRr7OA4r4x1b/kK3v/AF2f/wBCNZYpWsESpRRRXGUFFFFABRRRQAUUUUAFFFFABRRRQBd0XjWbD/r4j/8AQhX3qL18j92/HbbXwXofGtWH/XxH/wChCvvuJ4iXJdefetKfUmRBLfsEOY2GeOVpkd8qRgGN+ParNw8TKoDKefWpFkgC/wAPHvW8WZmNe3X2hwdvA9RVQn2qe6ZWmdh3NQcVqhkttEZpMDFXJLYom4BAw71FZ24kUnzGX6U6W3KsoE7c+taxYFhLWPy/niVi3c1X+zFpXjWMbB9Kka1cgYum/KqkVtM5crdEEHGfWmykSSWsaoxW3wwHBBFQi0EkYaRXyewNJcWl0EyLokE4pn2K9GALpfzrNlIo6tpaSxPEiv8AvUK8mvHNUt2st8Ey8qxyK9qmtL0yEG4UkD1ryfx7G8eqzJKctxyO/FcGLheNz2sqqu7pdGQaRDHcw5jHWnahb+WcYwKi8FyhL4K5yrAgD3xWrrGGBIGK8yF+p14ukqc+VM5uWMD2qAxqeuDVuQAmqlwrKMx9atnMJ9nRiQVGKgmsIuq4BqF7mZTjH40wSTSHAOKkLoY0LRNxzj0q/aMWUYzmmxx5xnrirVsgQ00mXEtNZ3DxB1G4Vlz7gxByDXe6QiNb8gdKqa5o0M0BkiAVx3Fb+ybV0NyVziPLlPRiKtW8Fw+BuNMkE9u5V0yB0Iq7pt2BIMis4ppkvlZYt7S4XB3NkVr2JnRx8x4qxAq3MYKY4q3b2xUgmumMTN2NmyzJDljzWRFsTU5Gl6ZxityxXCYrlNcdotUYLwN1KaYqUHOVkXUsvtPiSGZF+WNQxOK7K2ukTcz5DE9MVmaIIY7cSysA7qOtaatbtODuTGPWuqjC15dznx9dzkofyi3kscsXzKc9jg1VSGJkUoxDHtgmtRniYYEiY+tRWaRec3zL145rpPOKSxlW+YH8qsIK0ZYUaJjkHHTmqCjAxWkSR2018X6v/wAha9/67v8A+hGvtHrXxdq//IWvf+u7/wDoRrnxfQIlSiiiuMsKKKKACiiigAooooAKKKKACiiigC7ov/IYsP8ArvH/AOhCvvu3jj8oE2+c+1fAmif8hmw/6+I//QhX6GQriFRg9K1p7EyM2RITKg+zkfhSyx24ViLdwQP7pq+nzTs3Py8U2+kMdtIwPatYog5VwNxwDjNM4qWRuDmmR/M4HrWyAs2aAod+/H+zUqxRNIRmXA9jWlBhYwOMVHE3zSHg81rEZRliQIxEkowO61BHANuRcupPX5a1LgjyyMDnihAFVRjmhjRjyIQwUXRI68ilKSE5W5iP1rR63B46CpGwAcqMfSoLRirHMxYiWHPTrXHeOdIe4CTuquwBGV9hmvQ4YUK5ZByc1keJbZDabY1CuQcGsKq5lY3oVHTkmjwzTpTaaop24UMCK6HWOFx0rG1S2ls7xlmQqR+tbN+ftGmwzDGWUE148lZ2Z7M25e8YLHrULgkVMxAFQk80XM7EZjHpnNIIx6YqTrSZ9aNx8ogXHNSIP3igHvTeCOMU625nXPrVFI7LSRttg1aIAdMNyDVTTwFtVGKneUIK7YbEPcxr+wUMcDKntiqiabH1xz6VsSzAk9DUB6gioaVxJFnT4BCoAGKvqKpRScVahkyQKpOxMtDUt/ljznoKxZLD7fdmXBPzVpvIEjwe/FW9Cg81XIQEds1UVzEKo6Scy7b2Kx26I0IYgYyTUkFnE0r5hAA7VOtlzzbKfo9OgtVy3+isRns9dSVtDzKkuZ3Y2SztgBmIj6Co4LW2B+7L+AqW9i8qAlYZU99+aTTFZ0y/mnH901aRmPNvAsZKmQHtuFV1rRulRYOBNn/aqgoGK0WhDQAV8W6v/wAha9/67v8A+hGvtIcnFfFur/8AIWvf+u7/APoRrnxWyHEqUUUVxlhRRRQAUUUUAFFFFABRRRQAUUUUAXtD/wCQ1p//AF8R/wDoQr9CR5oHSP8AM1+e2hf8hvT/APr4j/8AQhX6Gk4jOa1p7MiZVt2kAYlQcn1qrrEsgt8FQAT61pxAhAAf0rJ16TmNCR6kVvEhGFIxPWnWjEzrgZpkpyTUmmgtPnHFdCWgzYMsqJ/qX4+lRRzMq/6qTnnpU8hwh6j8aVQQqgZ/OmCKs85LJmJxz6U83C90f/vk09iTOoyeKmYnaTnoPSpu2Mo28qtI7AEDp0qaaVBE3XNS2qfKSccmkulGxRgcmgq5Ek0QRQWA49ayNbmSWRQhyAK3WVc4ULjvWDq6J9qbZgADtUNFowLy2hnGJo0cf7QzWHrFqixFY1VUA4VRgV0si1laxATZs46dM1x14JwbOqhNqSVzzmRNrEVC45q3drtmYds1Wb2FecekmREe9Ru2KkY81FKhdCBwaLlkoRiBUtmp+0AHrmsqSS5UqR2q5BcEFWJ5ppitY7+y4t1xTL8/uCV6isqDUJI7UFELEj0qe3uJbiNvMj212KSsR1Ksc5dsZq6h4GazZ4zBOG/hNaMHzKKy6mjLa9qtWgO8GqsS5xitC1XGM81SMJs2rXTkukWR24z0zWvawrFIVjChQAKhsY5VgQIY+nfNWYhOS3+pPbvXbTStc8yrNt2LSqMZ25z3zT7ZRtPy96gBuB/BEcejVJbtP5f+ozz2YVsjBktwFMRyOKkt1AjBUHp2qvcPKIwGtiM/7QqWGRlVQYWHH1qrCE1U4tsEGsQE1q6rNuiC7GH1FZOTV9CSWMfNXxXq/wDyFr3/AK7v/wChGvtOM/NzXxZq/wDyFr3/AK7v/wChGuXE7IcSpRRRXIWFFFFABRRRQAUUUUAFFFFABRRRQBe0PnWtP7f6RH/6EK+/pbOZU/4+pDk96+AdC/5Den/9fEf/AKEK/QqQ/dFbU9mRMqC0uAOLh/zrE1BZFuGWRyxHcmukdsAknFcreSl5pGJ710wjcgpyE5q5pqTNkxOi/wC8M1Qc5NbWlrtiBHetxkrpd8AvE2T6UH7cOAkTfjip8s0qjPI5qYFsEkg0AZiG+8xj5CE9PvU+SW9CEtbDb04bNWrfJ3Hjk1JOT5YHHJqbjRWSe5SMD7KxA7ioJrud3UfZZRjtitVM7R1xTASbk4BwBSvYaKBv3XrbSg/7tYd3cGaZ3K4z2rrJG2gkjoM1ydwQ0jnHepbNEU3ptzEj6dKhYbyMjjvUrDJrTtEUQqCOvtWctdC4uzueK6kpW5fIxz0qlITt6V1vjzTxa6mzRg+W/wAw9q5GX0ryKseVtHqwlzJMhJyacP0qGUN0WoknkibEy5XswrFGhaxnqKQ2Q4cEjmojdRZ64q958UkI2OOK0jZ6D1Oi0Z0EAVlBrTOwjhcfSub0y6iRdrOAa1o51IyrZzXTCWliWR3ygDkZzTLVijAZ4qnquoCJ/LINSWlwsvllfxqXa4XZtwjmtK3Ul0xWbEeRjFa1pwdx6AVcXcwmzotMvIpGaFXXehwR6VowFiGx6+leN3GqXOl+KrtskZYHb2IwK7/QvEIv4wIJEEndG612Ql0PNmtTq+QpJ9Kmtm/cr0rKea9EZPlKR6ip4Jr0Io+zqR9a1RmXblsqOlSo3Tp+dZs9xcZAe3x9GqQXsy8fZZD9KsQmtuSEHFZOean1S6aeRcxtHjswqkCaLCsWYsFulfFur/8AIWvf+u7/APoRr7PgYAndXxhq/wDyFr3/AK7v/wChGufEbIcSpRRRXKUFFFFABRRRQAUUUUAFFFFABRRRQBe0L/kN6f8A9fEf/oQr9BzH8/EjcCvz40LjW9P/AOviP/0IV+gscgbc2eM10UFe5nMhvQy27kSnp0xXLTHOcmui1iULaketczIc12RViRgXLCty1inES+Xsx7msi2XMqjvXSwqAg6cVQEES3PmsdqEj3qWQ'
print(g:=s.find(61), s.find(61, g+1))
data = base64.b64decode(t,' /')
npdata = np.fromstring(data,dtype=np.uint8)
frame = cv2.imdecode(npdata,1)
cv2.imshow("s", frame)
key = cv2.waitKey(1) & 0xFF
if key == ord('q'):
    cv2.destroyAllWindows()