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
    turnover float,
    UNIQUE (instrument_id, trading_day));

alter table instrument add unique(instrument_id, trading_day);

create table if not exists RONGZI(
    data_id serial primary key,
    trading_day date,
    market char(4),
    rongzi_yue float,
    rongzi_mairu float,
    rongquan_yuliang float,
    rongquan_yuliang_jine float,
    rongquan_maichu float,
    UNIQUE (trading_day, market));

create table if not exists stock_info(
    stock_code varchar(8) primary key,
    stock_name varchar(32));

alter table RONGZI add unique(trading_day, market);

create table if not exists stock_info(
    stock_code varchar(8) primary key,
    stock_name varchar(32));

create table if not exists RONGZI_MINGXI (
    data_id serial primary key,
    trading_day date,
    market varchar(4),
    stock_code varchar(8) references stock_info(stock_code),
    rongzi_yue float,
    rongzi_mairu float,
    rongzi_changhuan float,
    rongquan_yuliang float,
    rongquan_maichu float,
    rongquan_changhuan float,
    UNIQUE (trading_day, stock_code));

create index rongzi_trading_day_idx on rongzi(trading_day);
create index rongzi_mingxi_trading_day_idx on rongzi_mingxi(trading_day);

create table if not exists holiday_type(
    type_id serial primary key,
    type_name  varchar(16)
);

create table if not exists holidays(
    holiday date primary key,
    type_id int references holiday_type(type_id));


