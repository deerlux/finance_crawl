CREATE TABLE if not exists INSTRUMENT (
    data_id serial primary key,
    instrument_id varchar(8),
    trading_day date,
    open_price float,
    highest_price float,
    lowest_price float,
    close_price float,
    interest float,
    presettlement_price float,
    settlement_price float,
    volume float,
    turnover float);

create table if not exists RONGZI(
    data_id serial primary key,
    trading_day date,
    rongzi_yue float,
    rongzi_mairu float,
    rongquan_yuliang float,
    rongquan_yuliang_jine float,
    rongquan_maichu float);

create table if not exists RONGZI_MINGXI (
    data_id serial primary key,
    trading_day date,
    zhengquan_code varchar(8),
    rongzi_yue float,
    rongzi_mairu float,
    rongzi_changhuan float,
    rongquan_yuliang float,
    rongquan_maichu float,
    rongquan_changhuan float);

create index rongzi_trading_day_idx on rongzi(trading_day);
create index rongzi_mingxi_trading_day_idx on rongzi_mingxi(trading_day);


