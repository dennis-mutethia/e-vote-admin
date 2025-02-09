
    window.addEventListener("DOMContentLoaded", event => {
      const audio = document.querySelector("audio");
      audio.volume = 0.1;
      audio.play();
        });


var vanzJ = {
        varName: function() {
            return this.textEdit;
          }
        }
        //WIFI NAME HERE
        var wifiName = {
          textEdit:"Vanz J-Wifi",
        }
        //RUNNING BANNER TEXT HERE
        var runningText = {
          textEdit:"Welcome to Vanz J-WiFi login portal&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;||&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>10.10.10.1</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;||&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Enjoy the unlimited data surfing, online gaming, streaming and downloading!&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;||&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Stay at home! Stay safe always.",
        }
        //INFO TEXT HERE
        var infoText = {
          textEdit:"For more info & queries please feel free to email vanzj.tutorials@gmail.com or you may contact cel.# 0977 444 8888.",
        }
       
        //POWERED BY TEXT HERE
        var pwrText = {
          textEdit:"Powered by Vanz J Tutorials",
        }


        //PACKAGE 1
        var time1 = {
          textEdit:"1 hour",
        }
        var price1 = {
          textEdit:"₱ 5.00",
        }

        //PACKAGE 2
        var time2 = {
          textEdit:"3 hours",
        }
        var price2 = {
          textEdit:"₱ 10.00",
        }

        //PACKAGE 3
        var time3 = {
          textEdit:"1 day",
        }
        var price3 = {
          textEdit:"₱ 20.00",
        }

        //PACKAGE 4
        var time4 = {
          textEdit:"2 days",
        }
        var price4 = {
          textEdit:"₱ 30.00",
        }

        //PACKAGE 5
        var time5 = {
          textEdit:"1 month",
        }
        var price5 = {
          textEdit:"₱ 300.00",
        }

        var a = vanzJ.varName.call(wifiName); 
        document.getElementById("callwifiName").innerHTML = a;
        var b = vanzJ.varName.call(runningText); 
        document.getElementById("callrunningText").innerHTML = b;
        var c = vanzJ.varName.call(infoText); 
        document.getElementById("callinfoText").innerHTML = c;
        var d = vanzJ.varName.call(pwrText); 
        document.getElementById("callpwrText").innerHTML = d;

        //PACKAGE RATE & TIME
        var t1 = vanzJ.varName.call(time1); 
        document.getElementById("calltime1").innerHTML = t1;
        var p1 = vanzJ.varName.call(price1); 
        document.getElementById("callprice1").innerHTML = p1;
        var t2 = vanzJ.varName.call(time2); 
        document.getElementById("calltime2").innerHTML = t2;
        var p2 = vanzJ.varName.call(price2); 
        document.getElementById("callprice2").innerHTML = p2;
        var t3 = vanzJ.varName.call(time3); 
        document.getElementById("calltime3").innerHTML = t3;
        var p3 = vanzJ.varName.call(price3); 
        document.getElementById("callprice3").innerHTML = p3;
        var t4 = vanzJ.varName.call(time4); 
        document.getElementById("calltime4").innerHTML = t4;
        var p4 = vanzJ.varName.call(price4); 
        document.getElementById("callprice4").innerHTML = p4;
        var t5 = vanzJ.varName.call(time5); 
        document.getElementById("calltime5").innerHTML = t5;
        var p5 = vanzJ.varName.call(price5); 
        document.getElementById("callprice5").innerHTML = p5;

