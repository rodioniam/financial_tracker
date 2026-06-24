from fastapi.responses import StreamingResponse
import io
import csv


async def export_transactions_csv(transactions_list):
    async def iter_tr():
        output = io.StringIO()  # создаю буфер
        writer = csv.writer(output)  # создаю объект для записи в буфер

        writer.writerow(['Дата', 'Сумма', 'Тип', 'Категория', 'Описание'])  # заголовок таблицы # noqa
        yield output.getvalue()  # возвращаю последнее значение в буфере
        output.seek(0)  # сбрасываю указатель записи на начало буфера
        output.truncate()  # очищаю буфер после создания заголовка

        for transaction in transactions_list:
            writer.writerow(
                [
                    transaction[0].date.strftime('%Y-%m-%d %H:%M'),
                    float(transaction[0].amount),
                    transaction[0].type.value,
                    transaction[1],
                    transaction[0].description
                ]
            )
            yield output.getvalue()
            output.seek(0)
            output.truncate()

    return StreamingResponse(
        iter_tr(),
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=transactions.csv'}
    )


async def export_sum_by_category_csv(result):
    async def iter_result():
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(
            [
                'Название категории',
                'Тип',
                'Сумма'
            ]
        )
        yield output.getvalue()
        output.seek(0)
        output.truncate()

        records = [r for r in result]
        for record in records:
            writer.writerow(
                [
                    record['name'],
                    record['type'],
                    record['sum']
                ]
            )
            yield output.getvalue()
            output.seek(0)
            output.truncate()

    return StreamingResponse(
        iter_result(),
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=categories_sum.csv'}
    )


async def export_monthly_stats_csv(result):
    async def iter_result():
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(
            [
                'Тип',
                'Год',
                'Месяц',
                'Сумма'
            ]
        )
        yield output.getvalue()
        output.seek(0)
        output.truncate()

        records = [r for r in result]

        for record in records:
            writer.writerow(
                [
                    record['type'],
                    record['year'],
                    record['month'],
                    record['amount']
                ]
            )
            yield output.getvalue()
            output.seek(0)
            output.truncate()

    return StreamingResponse(
        iter_result(),
        media_type='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=monthly_stats.csv'}
    )
