"""company_fields

Revision ID: 15a3abeff08b
Revises: 694c50f74f4a
Create Date: 2025-03-23 11:38:10.118284

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '15a3abeff08b'
down_revision = '694c50f74f4a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE TYPE translation_mode AS ENUM ('AUTO', 'USER');")
    op.add_column('company_fields', sa.Column('datetime_data', sa.DateTime(timezone=True), nullable=True))
    op.add_column('company_fields', sa.Column('is_translatable', sa.Boolean(), nullable=False))
    op.add_column('company_fields', sa.Column('translation_mode', sa.Enum('AUTO', 'USER', name='translation_mode'), nullable=True))
    op.drop_column('company_fields', 'translation_config')
    op.add_column('contacts', sa.Column('data', sa.Text(), nullable=False))
    op.drop_column('contacts', 'value')
    op.alter_column('financial_reports', 'annual_income',
               existing_type=sa.NUMERIC(precision=20, scale=2),
               nullable=True)
    op.alter_column('financial_reports', 'net_profit',
               existing_type=sa.NUMERIC(precision=20, scale=2),
               nullable=True)
    op.drop_constraint('financial_reports_audited_by_fkey', 'financial_reports', type_='foreignkey')
    op.drop_column('financial_reports', 'audited_by')
    op.drop_column('financial_reports', 'status')
    op.add_column('tax_reports', sa.Column('taxes_paid', sa.Text(), nullable=True))
    op.add_column('tax_reports', sa.Column('paid_insurance', sa.Text(), nullable=True))
    op.drop_column('tax_reports', 'status')
    op.drop_column('tax_reports', 'quarter')
    op.drop_column('tax_reports', 'period_start')
    op.drop_column('tax_reports', 'period_end')


def downgrade() -> None:
    op.add_column('tax_reports', sa.Column('period_end', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.add_column('tax_reports', sa.Column('period_start', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.add_column('tax_reports', sa.Column('quarter', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('tax_reports', sa.Column('status', postgresql.ENUM('DRAFT', 'SUBMITTED', 'VERIFIED', 'REJECTED', name='report_status'), autoincrement=False, nullable=False))
    op.drop_column('tax_reports', 'paid_insurance')
    op.drop_column('tax_reports', 'taxes_paid')
    op.add_column('financial_reports', sa.Column('status', postgresql.ENUM('DRAFT', 'SUBMITTED', 'VERIFIED', 'REJECTED', name='report_status'), autoincrement=False, nullable=False))
    op.add_column('financial_reports', sa.Column('audited_by', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('financial_reports_audited_by_fkey', 'financial_reports', 'users', ['audited_by'], ['id'])
    op.alter_column('financial_reports', 'net_profit',
               existing_type=sa.NUMERIC(precision=20, scale=2),
               nullable=False)
    op.alter_column('financial_reports', 'annual_income',
               existing_type=sa.NUMERIC(precision=20, scale=2),
               nullable=False)
    op.add_column('contacts', sa.Column('value', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_column('contacts', 'data')
    op.add_column('company_fields', sa.Column('translation_config', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_column('company_fields', 'translation_mode')
    op.drop_column('company_fields', 'is_translatable')
    op.drop_column('company_fields', 'datetime_data')
    op.execute("DROP TYPE translation_mode;")
