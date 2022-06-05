<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">Electricity Forecasting and Bidding</h3>

  <p align="center">
    DSAI HW3
    <br />
    <a href="https://github.com/Shulammiteya/Electricity-Forecasting-and-Bidding"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</p>


## data analysis

* y軸為：電力產量-電力用量，可以看出小時和月分都具備週期性。
<p float="center" align="center">
<img src="https://drive.google.com/uc?export=view&id=1rQFtksUbuaFMi4pp_ySpSCFpkZiZNtGJ" alt="data analysis">
</p>


## feature construction

* 加入小時指標，其值為 sin 和 cos 函數的總和，以 24 小時為一循環，藉此讓模型知道 23 點比 4 點更接近午夜 12 點。
<p float="center" align="center">
<img src="https://drive.google.com/uc?export=view&id=1RWOcdcGHSeLRIMBWvMW5GYCMaB-BWB2o" alt="hourly signal">
</p>

* 同樣加入月份指標，以 12 個月為一循環，保留週期性趨勢。
<p float="center" align="center">
<img src="https://drive.google.com/uc?export=view&id=1ZtvypJELKVllukWSGV-utD_CpbvSgXb5" alt="monthly signal">
</p>


## model training

* 使用 LSTM 模型進行多步預測，input 的 3 個特徵值分別為：電力差值，小時標記、月份標記。
<p float="center" align="center">
<img src="https://drive.google.com/uc?export=view&id=1Dh2Z0loshlj_EaehICi9e-6hbbOXJQMJ" alt="model structure">
</p>

* 模型訓練資訊。
<p float="center" align="center">
<img src="https://drive.google.com/uc?export=view&id=1J_sdUJSLLyDda4MVEX1x0wijVfB3cE8L" alt="training history">
</p>


## model validation

* 從 validation dataset 中隨機挑出 8 組做預測，輸入為前一星期的电量資訊，輸出為隔天的差值預測（電力產量-電力用量）。
<p float="center" align="center">
<img src="https://drive.google.com/uc?export=view&id=13SVkoR2A_C8Rg7riaNn1r8q84Lw6dH0G" alt="model validation">
</p>



<!-- CONTACT -->
## Contact

About me: [Hsin-Hsin, Chen](https://www.facebook.com/profile.php?id=100004017297228) - shulammite302332@gmail.com
