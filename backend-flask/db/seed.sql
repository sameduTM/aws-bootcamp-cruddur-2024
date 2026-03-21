-- this file was manually created
INSERT INTO public.users (display_name, email ,handle, cognito_user_id)
VALUES
  ('Ken Wekesa', 'wekesa884@gmail.com', 'wekesa884', 'MOCK'),
  ('Rachel Greene', 'samedutm@gmail.com', 'rachGreene' ,'MOCK');
  ('Londo Mollari', 'londomo@gmail.com', 'londo', 'MOCK')

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'wekesa884' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )
