# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """
    Migration script để xóa field rental_period khỏi database
    """
    _logger.info("Starting migration: removing rental_period field from obic.order")
    
    # Kiểm tra xem column có tồn tại không
    cr.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='obic_order' AND column_name='rental_period'
    """)
    
    if cr.fetchone():
        _logger.info("Column rental_period exists, removing...")
        
        # Xóa column khỏi database
        cr.execute("""
            ALTER TABLE obic_order 
            DROP COLUMN IF EXISTS rental_period
        """)
        
        _logger.info("Column rental_period removed successfully")
    else:
        _logger.info("Column rental_period does not exist, skipping")
    
    # Xóa field definition khỏi ir_model_fields nếu còn tồn tại
    cr.execute("""
        DELETE FROM ir_model_fields 
        WHERE model='obic.order' AND name='rental_period'
    """)
    
    _logger.info("Migration completed: rental_period field cleanup done")
