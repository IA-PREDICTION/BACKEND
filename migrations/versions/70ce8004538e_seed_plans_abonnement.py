from alembic import op
import sqlalchemy as sa

# révision
revision = "xxxx_seed_plans_abonnement"
down_revision = "82238e50ea1c" 
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
        INSERT INTO plans_abonnement
            (nom, description, prix, duree_jours, nb_pronostics_jour, sports_autorises,
             acces_stats_avancees, acces_predictions_ia, acces_historique_complet, acces_api,
             priority_support, periode_essai_jours, actif, ordre_affichage)
        VALUES
            ('Gratuit', 'Plan de découverte', 0.00, 0, 5, '["football"]'::jsonb, 
             false, true, false, false, false, 60, true, 1),
            ('Premium Mensuel', 'Accès complet mensuel', 9.99, 30, NULL, NULL,
             true, true, true, false, true, 0, true, 2),
            ('Premium Annuel', 'Accès complet annuel', 99.00, 365, NULL, NULL,
             true, true, true, true, true, 0, true, 3)
        ON CONFLICT DO NOTHING;
    """)

def downgrade():
    op.execute("""
        DELETE FROM plans_abonnement
        WHERE nom IN ('Gratuit', 'Premium Mensuel', 'Premium Annuel');
    """)
