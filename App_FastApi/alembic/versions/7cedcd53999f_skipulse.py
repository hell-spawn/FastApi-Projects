"""Skipulse

Revision ID: 7cedcd53999f
Revises: e30f1780feef
Create Date: 2024-06-10 18:29:12.063327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7cedcd53999f'
down_revision: Union[str, None] = 'e30f1780feef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cities',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Integer(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('population', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cities_country'), 'cities', ['country'], unique=False)
    op.create_index(op.f('ix_cities_id'), 'cities', ['id'], unique=False)
    op.create_index(op.f('ix_cities_name'), 'cities', ['name'], unique=False)
    op.create_table('weather',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('temperature', sa.Integer(), nullable=False),
    sa.Column('humidity', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_weather_city_id'), 'weather', ['city_id'], unique=False)
    op.create_index(op.f('ix_weather_description'), 'weather', ['description'], unique=False)
    op.create_index(op.f('ix_weather_humidity'), 'weather', ['humidity'], unique=False)
    op.create_index(op.f('ix_weather_id'), 'weather', ['id'], unique=False)
    op.create_index(op.f('ix_weather_temperature'), 'weather', ['temperature'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_weather_temperature'), table_name='weather')
    op.drop_index(op.f('ix_weather_id'), table_name='weather')
    op.drop_index(op.f('ix_weather_humidity'), table_name='weather')
    op.drop_index(op.f('ix_weather_description'), table_name='weather')
    op.drop_index(op.f('ix_weather_city_id'), table_name='weather')
    op.drop_table('weather')
    op.drop_index(op.f('ix_cities_name'), table_name='cities')
    op.drop_index(op.f('ix_cities_id'), table_name='cities')
    op.drop_index(op.f('ix_cities_country'), table_name='cities')
    op.drop_table('cities')
    # ### end Alembic commands ###
