CREATE USER grafana_user WITH PASSWORD 'postgres_grafana_pwd';

DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'taxi_monitoring') THEN
      CREATE DATABASE taxi_monitoring;
      GRANT ALL PRIVILEGES ON DATABASE taxi_monitoring TO grafana_user;
   END IF;
END
$$;
